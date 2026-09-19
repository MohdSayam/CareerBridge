from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from datetime import datetime

from app.models import User, db, Student, Company, JobPosition, Application, Placement
from app.cache import cache

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/api/student"
)

def get_current_student():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user or user.role!= "student":
        return None
    
    if not user.is_active:
        return None
    
    student = Student.query.filter_by(user_id=user.id).first()

    if not student:
        return None
    
    if student.is_blacklisted:
        return None
    
    return student

@student_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    student = get_current_student() 

    if not student:
        return jsonify({
            "message":"Unauthorized"
        }), 403

    # Manual Redis caching (per-student key)
    cache_key = f"student_dashboard_{student.id}"
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached), 200
    
    available_jobs = (
        JobPosition.query
        .join(Company)
        .filter(
            Company.approval_status == "approved",
            Company.is_blacklisted == False,
            JobPosition.status == "approved",
            JobPosition.application_deadline >= datetime.utcnow()
        ).count()
    )

    applications = Application.query.filter_by(student_id=student.id).count()
    
    shortlisted = Application.query.filter_by(student_id=student.id, status="shortlisted").count()

    interviews = Application.query.filter_by(student_id=student.id, status="interview").count()

    selected = Application.query.filter_by(student_id=student.id, status="selected").count()

    placed = Application.query.filter_by(student_id=student.id, status="placed").count()

    upcoming_interview_apps = (
        Application.query
        .filter_by(student_id=student.id, status="interview")
        .filter(Application.interview_date != None)
        .order_by(Application.interview_date.asc())
        .limit(3).all()
    )
    upcoming_interviews = []
    for a in upcoming_interview_apps:
        upcoming_interviews.append({
            "application_id": a.id,
            "job_title": a.job.title if a.job else "Unknown",
            "company_name": a.job.company.company_name if a.job and a.job.company else "Unknown",
            "interview_date": a.interview_date.isoformat() if a.interview_date else None
        })

    latest_job_records = (
        JobPosition.query
        .join(Company)
        .filter(
            Company.approval_status == "approved",
            Company.is_blacklisted == False,
            JobPosition.status == "approved",
            JobPosition.application_deadline >= datetime.utcnow()
        )
        .order_by(JobPosition.id.desc())
        .limit(3).all()
    )
    
    latest_jobs = []
    for j in latest_job_records:
        latest_jobs.append({
            "id": j.id,
            "title": j.title,
            "company": j.company.company_name if j.company else "Unknown",
            "salary_range": j.salary_range,
            "application_deadline": j.application_deadline.isoformat(timespec="minutes") if j.application_deadline else ""
        })

    latest_app_records = (
        Application.query
        .filter_by(student_id=student.id)
        .order_by(Application.id.desc())
        .limit(3).all()
    )
    
    latest_applications = []
    for a in latest_app_records:
        latest_applications.append({
            "id": a.id,
            "job_title": a.job.title if a.job else "Unknown",
            "company_name": a.job.company.company_name if a.job and a.job.company else "Unknown",
            "status": a.status,
            "applied_on": a.applied_at.isoformat() if a.applied_at else None
        })

    result = {
        "available_jobs": available_jobs,
        "applications": applications,
        "shortlisted": shortlisted,
        "interviews": interviews,
        "selected": selected,
        "placed": placed,
        "upcoming_interviews": upcoming_interviews,
        "latest_jobs": latest_jobs,
        "latest_applications": latest_applications
    }
    cache.set(cache_key, result, timeout=120)  # 2 min cache
    return jsonify(result), 200

@student_bp.route("/jobs", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300, key_prefix="student_jobs")
def get_jobs():
    student = get_current_student()

    if not student:
        return jsonify({
            "message":"Unauthorized"
        }), 403
    
    jobs = (
        JobPosition.query
        .join(Company)
        .filter(
            Company.approval_status == "approved",
            Company.is_blacklisted == False,
            JobPosition.status == "approved",
            JobPosition.application_deadline >= datetime.utcnow()
        ).all()
    )

    result = []

    for job in jobs:
        result.append({
            "id": job.id,
            "company": job.company.company_name,
            "title": job.title,
            "description": job.description,
            "salary_range": job.salary_range,
            "skills_required": job.skills_required,
            "minimum_cgpa": job.minimum_cgpa,
            "eligible_branch": job.eligible_branch,
            "eligible_year": job.eligible_year,
            "application_deadline": (
                job.application_deadline.isoformat(timespec="minutes")
                if job.application_deadline
                else ""
            )
        })

    return jsonify(result), 200

@student_bp.route("/jobs/search", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def search_jobs():
    student = get_current_student() 

    if not student:
        return jsonify({
            "message": "Unauthorized"
        }), 403
    
    search = request.args.get("search")

    query = (
        JobPosition.query
        .join(Company)
        .filter(
            Company.approval_status == "approved",
            Company.is_blacklisted == False,
            JobPosition.status == "approved",
            JobPosition.application_deadline >= datetime.utcnow()
        )
    )

    if search:
        query = query.filter(
            or_(
                Company.company_name.ilike(f"%{search}%"),
                JobPosition.title.ilike(f"%{search}%"),
                JobPosition.skills_required.ilike(f"%{search}%")
            )
        )
    
    jobs = query.all()

    result = []

    for job in jobs:
        result.append({
            "id": job.id,
            "company": job.company.company_name,
            "company_id": job.company_id,
            "title": job.title,
            "description": job.description,
            "salary_range": job.salary_range,
            "minimum_cgpa": job.minimum_cgpa,
            "eligible_branch": job.eligible_branch,
            "eligible_year": job.eligible_year,
            "application_deadline": job.application_deadline.isoformat() if job.application_deadline else None,
            "skills_required": job.skills_required,
            "experience_required": job.experience_required
        })
    
    return jsonify(result), 200
@student_bp.route("/job/<int:job_id>", methods=["GET"])
@jwt_required()
def get_job_details(job_id):
    student = get_current_student()
    if not student:
        return jsonify({"message": "Unauthorized"}), 403
        
    job = JobPosition.query.get(job_id)
    if not job or job.status != "approved":
        return jsonify({"message": "Job not found or not active"}), 404
        
    company = Company.query.filter_by(id=job.company_id).first()
    
    return jsonify({
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "salary_range": job.salary_range,
        "minimum_cgpa": job.minimum_cgpa,
        "eligible_branch": job.eligible_branch,
        "eligible_year": job.eligible_year,
        "application_deadline": job.application_deadline.isoformat() if job.application_deadline else None,
        "skills_required": job.skills_required,
        "experience_required": job.experience_required,
        "company": {
            "id": company.id,
            "name": company.company_name,
            "description": company.description,
            "industry": company.industry,
            "website": company.website,
            "location": company.location
        }
    }), 200


@student_bp.route("/job/<int:job_id>/apply", methods=["POST"])
@jwt_required()
def apply_job(job_id):
    student = get_current_student() 

    if not student:
        return jsonify({
            "message": "Unauthorized"
        }), 403
    
    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "message": "job not found"
        }), 404
    
    company = job.company

    if company.approval_status != "approved":
        return jsonify({
            "message": "Company is not approved"
        }), 400
    
    if company.is_blacklisted:
        return jsonify({
            "message": "Company is blacklisted"
        }), 400
    
    if job.status != "approved":
        return jsonify({
            "message": "Job is not available"
        }), 400
    
    if job.application_deadline < datetime.utcnow():
        return jsonify({
            "message": "Job deadline is passed"
        }), 400
    

    # prevention to duplicate application
    existing = Application.query.filter_by(student_id=student.id, job_id=job.id).first()

    if existing:
        return jsonify({
            "message": "You have already applied"
        }), 400
    
    application = Application(
        student_id = student.id,
        job_id = job.id
    )

    db.session.add(application)
    db.session.commit()

    # Invalidate student caches so dashboard/applications reflect new data
    cache.delete(f"student_dashboard_{student.id}")
    cache.delete(f"student_applications_{student.id}")

    return jsonify({
        "message": "Application submitted successfully"
    }), 201

@student_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_applications():
    student = get_current_student() 

    if not student:
        return jsonify({
            "message": "Unauthorized"
        }), 403

    # Manual Redis caching (per-student key)
    cache_key = f"student_applications_{student.id}"
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached), 200
    
    applications = Application.query.filter_by(student_id=student.id).all()

    result = []

    for application in applications:
        job = application.job
        company = job.company

        result.append({
            "application_id": application.id,
            "company": company.company_name,
            "job_title": job.title,
            "salary_range": job.salary_range,
            "status": application.status,
            # NOTE: 'feedback' (company private notes) intentionally excluded from student view
            "interview_date": application.interview_date.isoformat() if application.interview_date else None,
            "applied_at": application.applied_at.isoformat() if application.applied_at else None
        })

    cache.set(cache_key, result, timeout=120)  # 2 min cache
    return jsonify(result), 200

@student_bp.route("/placements", methods=["GET"])
@jwt_required()
def get_placements():

    student = get_current_student()

    if not student:
        return jsonify({
            "message": "Unauthorized"
        }), 403

    placements = (
        Placement.query
        .join(Application)
        .filter(Application.student_id == student.id)
        .all()
    )

    result = []

    for placement in placements:

        application = placement.application
        job = application.job
        company = job.company

        result.append({
            "placement_id": placement.id,
            "company": company.company_name,
            "job_title": job.title,
            "salary": placement.salary,
            "joining_date": placement.joining_date,
            "offer_letter_path": placement.offer_letter_path,
            "placed_on": placement.placed_on
        })

    return jsonify(result), 200


@student_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    student = get_current_student()

    if not student:
        return jsonify({
            "message": "Unauthorized"
        }), 403

    return jsonify({
        "full_name": student.full_name,
        "education": student.education,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "experience": student.experience,
        "skills": student.skills,
        "resume_path": student.resume_path,
        "profile_picture_url": student.profile_picture_url or ""
    }), 200

@student_bp.route("/profile", methods=["PATCH"])
@jwt_required()
def update_profile():  
    student = get_current_student()

    if not student:
        return jsonify({
            "message": "Unauthorized"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    if "education" in data:
        student.education = data["education"]

    if "branch" in data:
        student.branch = data["branch"]

    if "cgpa" in data:
        student.cgpa = data["cgpa"]

    if "graduation_year" in data:
        student.graduation_year = data["graduation_year"]

    if "experience" in data:
        student.experience = data["experience"]

    if "skills" in data:
        student.skills = data["skills"]

    if "resume_path" in data:
        student.resume_path = data["resume_path"]

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200

@student_bp.route("/export", methods=["POST"])
@jwt_required()
def export_csv():
    student = get_current_student()

    if not student:
        return jsonify({
            "message": "Unauthorized"
        }), 403
    
    from app.tasks import export_student_applications

    export_student_applications.delay(student.id)

    return jsonify({
        "message": "CSV export started. You will recieve an email shortly"
    }), 202