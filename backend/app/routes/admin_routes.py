from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import db, User, Student, Company, JobPosition, Application, Placement
from app.cache import cache
from sqlalchemy import or_ 

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)

def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    return user and user.role == "admin"

@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    if not is_admin():
        return jsonify({
            "message":"Unauthorized access"
        }), 403
    
    student_count = Student.query.count()
    company_count = Company.query.count()
    job_count = JobPosition.query.count()
    application_count = Application.query.count()

    approved_companies = Company.query.filter_by(approval_status="approved").count()
    approved_jobs = JobPosition.query.filter_by(status="approved").count()
    placed_students = Placement.query.count()

    shortlisted = Application.query.filter_by(status="shortlisted").count()
    interviews = Application.query.filter_by(status="interview").count()
    selected = Application.query.filter_by(status="selected").count()
    rejected = Application.query.filter_by(status="rejected").count()

    return jsonify({
        "student_count": student_count,
        "company_count": company_count,
        "job_count": job_count,
        "application_count": application_count,
        "approved_companies": approved_companies,
        "approved_jobs": approved_jobs,
        "shortlisted":shortlisted,
        "interviews":interviews,
        "selected": selected,
        "rejected": rejected,
        "placed_students": placed_students
    }), 200

@admin_bp.route("/companies", methods=["GET"])
@jwt_required()
def get_companies():

    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403

    companies = Company.query.all()
    result = []
    for company in companies:
        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location" : company.location,
            "approval_status": company.approval_status,
            "is_blacklisted": company.is_blacklisted,
            "website": company.website,
            "description": company.description,
            "profile_picture_url": company.profile_picture_url
        })

    return jsonify(result), 200

@admin_bp.route("/company/<int:company_id>/status", methods=["PATCH"])
@jwt_required()
def update_company_status(company_id):
    if not is_admin():
        return jsonify({
            "message": "Unauthorized access"
        }), 403
    
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            "message": "Company Not Found"
        }), 404
    
    allowed_status = ["pending", "approved", "rejected"]

    data = request.get_json()
    status = data.get("approval_status")

    if status not in allowed_status:
        return jsonify({
            "message":"Invalid status"
        }), 400
    
    company.approval_status = status
    db.session.commit()

    cache.clear()

    messages = {
    "approved": "Company approved successfully",
    "rejected": "Company rejected successfully",
    "pending": "Company status changed to pending"
    }

    return jsonify({
        "message": messages[status]
    }), 200

@admin_bp.route("/company/<int:company_id>/blacklist", methods=["PATCH"])
@jwt_required()
def blacklist_company(company_id):
    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403

    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    company.is_blacklisted = (not company.is_blacklisted)
    db.session.commit()

    cache.clear()

    message = ("company blacklisted successfully" if company.is_blacklisted else "Company removed from blacklist")

    return jsonify({
        "message": message
    }), 200

@admin_bp.route("/companies/search", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def search_companies():
    if not is_admin():
        return jsonify({
            "message": "Unauthorized acess"
        }), 403
    
    search = request.args.get("search")

    if search:
        companies = Company.query.filter(
            or_(
                Company.company_name.ilike(f"%{search}%"),
                Company.industry.ilike(f"%{search}%"),
            )
        ).all()
    else:
        companies = Company.query.all()    
    result = []

    for company in companies:
        result.append({
            "id":company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location" : company.location,
            "approval_status": company.approval_status,
            "is_blacklisted": company.is_blacklisted,
            "website": company.website,
            "description": company.description,
            "profile_picture_url": company.profile_picture_url
        })

    return jsonify(result), 200

@admin_bp.route("/students", methods=["GET"])
@jwt_required()
def get_students():
    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403
    
    students = Student.query.all()
    result = []

    for student in students:
        result.append({
            "id": student.id,
            "full_name":student.full_name,
            "education":student.education,
            "branch":student.branch,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "is_blacklisted":student.is_blacklisted,
            "resume_path": student.resume_path,
            "profile_picture_url": student.profile_picture_url
        })

    return jsonify(result), 200

@admin_bp.route("/student/<int:student_id>/blacklist", methods=["PATCH"])
@jwt_required()
def blacklist_student(student_id):
    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403
    
    student = Student.query.get(student_id)
    if not student:
        return jsonify({
            "message":"Student not found"
        }), 404
    
    student.is_blacklisted = (not student.is_blacklisted)
    db.session.commit()

    cache.clear()

    message = ("Student blacklisted successfully" if student.is_blacklisted else "Student removed from blacklist")
    return jsonify({
        "message": message
    }), 200

@admin_bp.route("/students/search", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300, query_string=True)
def search_students():
    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403
    
    search = request.args.get("search")

    if search:
        students = Student.query.filter(
            or_(
                Student.full_name.ilike(f"%{search}%"),
                Student.branch.ilike(f"%{search}%"),
            )
        ).all()
    else:
        students = Student.query.all()

    result = []
    for student in students:
        result.append({
            "id": student.id,
            "full_name": student.full_name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "graduation_year":student.graduation_year,
            "is_blacklisted": student.is_blacklisted,
            "resume_path": student.resume_path,
            "profile_picture_url": student.profile_picture_url
        })

    return jsonify(result), 200

@admin_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_jobs():
    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403

    jobs = JobPosition.query.all()
    result = []

    for job in jobs:
        company = job.company
        result.append({
            "id": job.id,
            "company_id": job.company_id,
            "company_name": company.company_name if company else "Unknown",
            "title": job.title,
            "salary_range": job.salary_range,
            "minimum_cgpa": job.minimum_cgpa,
            "eligible_branch": job.eligible_branch,
            "eligible_year": job.eligible_year,
            "status": job.status
        })

    return jsonify(result), 200

@admin_bp.route("/job/<int:job_id>/status", methods=["PATCH"])
@jwt_required()
def update_job_status(job_id):
    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403

    job = JobPosition.query.get(job_id)

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404

    data = request.get_json()
    allowed_status = ["pending", "approved", "rejected", "closed"]
    status = data.get("status")

    if status not in allowed_status:
        return jsonify({
            "message": "Invalid status"
        }), 400

    job.status = status
    db.session.commit()

    cache.delete("student_jobs")

    messages = {
    "approved": "Admin approved this job",
    "rejected": "Admin rejected this job",
    "pending": "Job status changed to pending by admin",
    "closed": "Admin closed this job",
    }

    return jsonify({
        "message": messages[status]
    }), 200

@admin_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_applications():
    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403
    
    applications = Application.query.all()
    result = []

    for application in applications:
        student = application.student
        job = application.job
        company = job.company if job else None

        result.append({
            "id": application.id,
            "student_id": application.student_id,
            "student_name": student.full_name if student else "Unknown",
            "job_id": application.job_id,
            "job_title": job.title if job else "Unknown",
            "company_name": company.company_name if company else "Unknown",
            "status": application.status,
            "applied_at": application.applied_at.isoformat() + "Z" if application.applied_at else None,
            "feedback": application.feedback,
            "interview_date": application.interview_date.isoformat() + "Z" if application.interview_date else None
        })

    return jsonify(result), 200

@admin_bp.route("/placements", methods=["GET"])
@jwt_required()
def get_placements():
    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403
    
    placements = Placement.query.all()
    result = []

    for placement in placements:
        app = placement.application
        student = app.student if app else None
        job = app.job if app else None
        company = job.company if job else None

        result.append({
            "id": placement.id,
            "application_id": placement.application_id,
            "student_name": student.full_name if student else "Unknown",
            "job_title": job.title if job else "Unknown",
            "company_name": company.company_name if company else "Unknown",
            "salary": placement.salary,
            "joining_date": placement.joining_date.isoformat() + "Z" if placement.joining_date else None,
            "offer_letter_path": placement.offer_letter_path,
            "placed_on": placement.placed_on.isoformat() + "Z" if placement.placed_on else None
        })

    return jsonify(result), 200

@admin_bp.route("/interviews", methods=["GET"])
@jwt_required()
def get_interviews():
    if not is_admin():
        return jsonify({
            "message": "Unauthorized"
        }), 403
    
    applications = Application.query.filter(
        Application.interview_date != None
    ).all()
    
    result = []
    for app in applications:
        student = app.student
        job = app.job
        company = job.company
        
        result.append({
            "application_id": app.id,
            "student_name": student.full_name,
            "company_name": company.company_name,
            "job_title": job.title,
            "interview_date": app.interview_date.isoformat() + "Z", # We ensure it is parsed as UTC by frontend
            "status": app.status,
            "feedback": app.feedback or ""
        })
        
    return jsonify(result), 200