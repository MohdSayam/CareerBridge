import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

from app.models import User, db, Company, JobPosition, Application, Student, Placement
from app.cache import cache
from app.mail import mail
from flask_mail import Message

company_bp = Blueprint(
    "company",
    __name__,
    url_prefix="/api/company"
)

VALID_APPLICATION_TRANSITIONS = {
    "applied": ["shortlisted", "rejected"],
    "shortlisted": ["interview", "rejected"],
    "interview": ["selected", "rejected"],
    "selected": ["placed", "rejected"],
    "placed": [],
    "rejected": []
}

def get_current_company():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user or user.role != "company":
        return None 

    company = Company.query.filter_by(user_id=user.id).first()

    if not company:
        return None 

    if company.approval_status != "approved":
        return "pending"

    if company.is_blacklisted:
        return "blacklisted"

    if not user.is_active:
        return "inactive"

    return company 

def validate_company(company):
    if company=="pending":
        return jsonify({
            "message": "Company profile is waiting for admin approval"
        }), 403
    
    if company == "blacklisted":
        return jsonify({
            "message": "Your company has been blacklisted."
        }), 403

    if company == "inactive":
        return jsonify({
            "message": "Your account is inactive."
        }), 403

    if not company:
        return jsonify({
            "message": "Unauthorized"
        }), 403

    return None

@company_bp.route("/dashboard", methods=["GET"]) 
@jwt_required()
def dashboard():
    company = get_current_company()
    response = validate_company(company) 

    if response:
        return response

    # Manual Redis caching (per-company key)
    cache_key = f"company_dashboard_{company.id}"
    cached = cache.get(cache_key)
    if cached:
        return jsonify(cached), 200
    
    jobs = JobPosition.query.filter_by(company_id=company.id).count()

    applications = (
        Application.query
        .join(JobPosition)
        .filter(JobPosition.company_id==company.id)
        .count()
    )    

    shortlisted = (
        Application.query
        .join(JobPosition)
        .filter(
            JobPosition.company_id == company.id,
            Application.status == "shortlisted"
        )
        .count()
    )

    interviews = (
        Application.query
        .join(JobPosition)
        .filter(
            JobPosition.company_id==company.id,
            Application.status == "interview"
        )
        .count()
    )
    selected = (
        Application.query
        .join(JobPosition)
        .filter(
            JobPosition.company_id==company.id,
            Application.status == "selected"
        )
        .count()
    )

    placed = (
        Application.query
        .join(JobPosition)
        .filter(
            JobPosition.company_id==company.id,
            Application.status == "placed"
        )
        .count()
    )

    active_jobs = (
        JobPosition.query
        .filter_by(
            company_id=company.id,
            status="approved"
        )
        .count()
    )

    upcoming_interview_apps = (
        Application.query
        .join(JobPosition)
        .filter(
            JobPosition.company_id == company.id,
            Application.status == "interview",
            Application.interview_date != None
        )
        .order_by(Application.interview_date.asc())
        .limit(5).all()
    )
    upcoming_interviews = []
    for a in upcoming_interview_apps:
        upcoming_interviews.append({
            "application_id": a.id,
            "job_title": a.job.title if a.job else "Unknown",
            "student_name": a.student.full_name if a.student else "Unknown",
            "interview_date": a.interview_date.isoformat() if a.interview_date else None
        })

    recent_app_records = (
        Application.query
        .join(JobPosition)
        .filter(JobPosition.company_id == company.id)
        .order_by(Application.id.desc())
        .limit(5).all()
    )
    recent_applications = []
    for a in recent_app_records:
        recent_applications.append({
            "id": a.id,
            "student_name": a.student.full_name if a.student else "Unknown",
            "job_title": a.job.title if a.job else "Unknown",
            "status": a.status,
            "applied_on": a.applied_at.isoformat() if a.applied_at else None
        })

    result = {
        "jobs": jobs,
        "active_jobs": active_jobs,
        "applications": applications,
        "shortlisted": shortlisted,
        "interviews": interviews,
        "selected": selected,
        "placed": placed,
        "upcoming_interviews": upcoming_interviews,
        "recent_applications": recent_applications
    }
    cache.set(cache_key, result, timeout=120)  # 2 min cache
    return jsonify(result), 200


@company_bp.route("/interviews", methods=["GET"])
@jwt_required()
def get_all_interviews():
    company = get_current_company()
    response = validate_company(company)
    if response:
        return response

    interview_apps = (
        Application.query
        .join(JobPosition)
        .filter(
            JobPosition.company_id == company.id,
            Application.interview_date != None
        )
        .order_by(Application.interview_date.desc())
        .all()
    )

    result = []
    for a in interview_apps:
        result.append({
            "application_id": a.id,
            "job_title": a.job.title if a.job else "Unknown",
            "student_name": a.student.full_name if a.student else "Unknown",
            "interview_date": a.interview_date.isoformat() if a.interview_date else None,
            "status": a.status
        })

    return jsonify(result), 200


@company_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    company = get_current_company()
    response = validate_company(company)

    if response:
        return response
    
    return jsonify({
        "company_name": company.company_name,
        "industry": company.industry,
        "location": company.location,
        "website": company.website,
        "description": company.description,
        "profile_picture_url": company.profile_picture_url or ""
    }), 200


@company_bp.route("/profile", methods=["PATCH"])
@jwt_required()
def update_profile():
    company = get_current_company()
    response = validate_company(company)

    if response:
        return response
    
    data = request.get_json()
    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400
    
    if "industry" in data:
        company.industry = data["industry"]

    if "location" in data:
        company.location = data["location"]

    if "website" in data:
        company.website = data["website"]

    if "description" in data:
        company.description = data["description"]

    db.session.commit()

    return jsonify({
        "message": "Company profile updated successfully"
    }), 200

@company_bp.route("/jobs", methods=["POST"])
@jwt_required()
def create_jobs():
    company = get_current_company() 
    response = validate_company(company) 

    if response:
        return response
    
    data = request.get_json()
    if not data:
        return jsonify({
            "message":"No data provided"
        }), 400
    
    required_fields = [
        "title",
        "description",
        "salary_range",
        "application_deadline"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400
            
    if data.get('minimum_cgpa') is not None:
        if float(data.get('minimum_cgpa')) < 0 or float(data.get('minimum_cgpa')) > 10:
            return jsonify({
                "message":"CGPA must be between 0 and 10"
            }), 400
    
    try:
        deadline=datetime.fromisoformat(data.get("application_deadline"))
    except ValueError:
        return jsonify({
            "message": "Invalid application deadline format"
        }), 400
    
    job = JobPosition(
        company_id=company.id,
        title=data.get("title"),
        description=data.get("description"),
        salary_range=data.get("salary_range"),
        skills_required=data.get("skills_required"),
        experience_required=data.get("experience_required"),
        minimum_cgpa=data.get("minimum_cgpa", 0.0),
        eligible_branch=data.get("eligible_branch", ""),
        eligible_year=data.get("eligible_year", 0),
        application_deadline=deadline,
        status="approved"
    )

    try:
        db.session.add(job)
        db.session.commit()

        cache.delete("student_jobs")

        return jsonify({
            "message": "Job created successfully"
        }), 201
    
    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Unable to create a job",
            "error" : str(e)
        }), 500
    

@company_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_jobs():
    company = get_current_company()
    response = validate_company(company) 

    if response:
        return response
    
    jobs = JobPosition.query.filter_by(company_id=company.id).all()
    result = []

    for job in jobs: 
        result.append({
            "id": job.id,
            "title": job.title,
            "salary_range": job.salary_range,
            "minimum_cgpa": job.minimum_cgpa,
            "experience_required": job.experience_required,
            "eligible_branch": job.eligible_branch,
            "eligible_year": job.eligible_year,
            "status": job.status,
            "created_at": job.created_at.isoformat() if job.created_at else None,
            "application_deadline": (
                job.application_deadline.isoformat(timespec="minutes")
                if job.application_deadline
                else ""
            )
        })
    
    return jsonify(result), 200


@company_bp.route("/job/<int:job_id>", methods=["PATCH"])
@jwt_required()
def update_job(job_id):
    company = get_current_company()
    response = validate_company(company) 

    if response:
        return response
    
    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first()

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404
    
    data = request.get_json()

    if not data:
        return jsonify({
            "message":"No data provided"
        }), 400

    if "title" in data:
        job.title = data["title"]

    if "description" in data:
        job.description = data["description"]
    
    if "salary_range" in data:
        job.salary_range = data["salary_range"]

    if "skills_required" in data:
        job.skills_required = data["skills_required"]

    if "experience_required" in data:
        job.experience_required = data["experience_required"]

    if "minimum_cgpa" in data:
        job.minimum_cgpa = data["minimum_cgpa"]

    if "eligible_branch" in data:
        job.eligible_branch = data["eligible_branch"]

    if "eligible_year" in data:
        job.eligible_year = data["eligible_year"]

    if "application_deadline" in data:
        try:
            job.application_deadline = datetime.fromisoformat(
                data["application_deadline"]
            )
        except ValueError:
            return jsonify({
                "message":"Invalid application deadline format"
            }), 400

    db.session.commit()

    cache.delete("student_jobs")

    return jsonify({
        "message": "Job updated successfully and sent for admin review"
    }), 200

@company_bp.route("/job/<int:job_id>/status", methods=["PATCH"])
@jwt_required()
def close_job_status(job_id):
    company = get_current_company() 
    response = validate_company(company)

    if response:
        return response
    
    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first()

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404
    
    data = request.get_json()

    status = data.get("status")

    if status not in ["closed", "approved"]:
        return jsonify({
            "message": "Company can only close or re-open jobs"
        }), 400

    job.status = status

    db.session.commit()

    cache.delete("student_jobs")

    return jsonify({
        "message": f"Job {status} successfully"
    }), 200
    

@company_bp.route("/job/<int:job_id>/applications", methods=["GET"])
@jwt_required()
def get_job_applications(job_id):
    company = get_current_company()
    response = validate_company(company) 

    if response:
        return response
    
    job = JobPosition.query.filter_by(id=job_id, company_id=company.id).first()

    if not job:
        return jsonify({
            "message": "Job not found"
        }), 404
    
    applications = Application.query.filter_by(job_id=job.id).all()

    result = []

    for application in applications:
        student = application.student

        result.append({
            "application_id": application.id,
            "student_id": student.id,
            "student_name": student.full_name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "skills": student.skills,
            "profile_picture_url": student.profile_picture_url,
            "resume_path": student.resume_path,
            "status": application.status,
            "feedback": application.feedback or "",
            "interview_date": (
                application.interview_date.isoformat(timespec="minutes")
                if application.interview_date
                else ""
            )
        })

    return jsonify(result), 200


from datetime import datetime, timezone, timedelta

@company_bp.route("/application/<int:application_id>", methods=["PATCH", "GET"])
@jwt_required()
def update_application(application_id):
    company = get_current_company()
    response = validate_company(company) 

    if response:
        return response

    application = (
        Application.query
        .join(JobPosition)
        .filter(
            Application.id == application_id,
            JobPosition.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({
            "message": "Application not found"
        }), 404

    if request.method == "GET":
        student = application.student
        return jsonify({
            "application_id": application.id,
            "status": application.status,
            "applied_at": application.applied_at.isoformat() if application.applied_at else None,
            "feedback": application.feedback or "",
            "interview_date": application.interview_date.isoformat() if application.interview_date else None,
            "interview_link": application.interview_link or "",
            "student_id": student.id,
            "student_name": student.full_name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "education": student.education,
            "graduation_year": student.graduation_year,
            "skills": student.skills,
            "experience": student.experience,
            "job_id": application.job_id,
            "job_title": application.job.title,
            "profile_picture_url": student.profile_picture_url,
            "resume_path": student.resume_path
        }), 200

    job = application.job
    data = request.get_json()

    if "status" in data:
        new_status = data["status"]
        current_status = application.status

        if new_status not in VALID_APPLICATION_TRANSITIONS[current_status]:
            return jsonify({
                "message": "Invalid status transition"
            }), 400

        application.status = new_status

        if new_status == "placed":
            joining_date = None
            if data.get("joining_date"):
                try:
                    joining_date = datetime.fromisoformat(
                        data["joining_date"]
                    )
                    
                    ist_today = (datetime.utcnow() + timedelta(hours=5, minutes=30)).date()
                    if joining_date.date() < ist_today:
                        return jsonify({
                            "message": "Joining date cannot be in the past"
                        }), 400
                        
                except ValueError:
                    return jsonify({
                        "message": "Invalid joining date format"
                    }), 400

            existing_placement = Placement.query.filter_by(
                application_id=application.id
            ).first()

            if not existing_placement:
                placement = Placement(
                    application_id=application.id,
                    salary=job.salary_range,
                    joining_date=joining_date,
                    offer_letter_path=""
                )
                db.session.add(placement)
                db.session.flush()  # get placement id
                
                # Generate and email offer letter — wrapped so SMTP failure never blocks placement
                try:
                    _send_offer_letter_email(application, job, student, joining_date)
                except Exception as email_err:
                    import logging
                    logging.getLogger(__name__).warning(
                        f"Offer letter email failed for application {application.id}: {email_err}"
                    )
                
            elif joining_date:
                existing_placement.joining_date = joining_date

    if "feedback" in data:
        application.feedback = data["feedback"]

    if "interview_date" in data:
        if data["interview_date"]:
            try:
                dt_raw = data["interview_date"]
                # Treat value from datetime-local input as IST directly (strip any Z/offset)
                dt_raw_clean = dt_raw.replace('Z', '').split('+')[0].split('-')[0:3]
                # Use fromisoformat cleanly — strip timezone info, treat as IST naive datetime
                dt = datetime.fromisoformat(dt_raw.replace('Z', '').split('.')[0])
                application.interview_date = dt
            except ValueError:
                return jsonify({
                    "message": "Invalid interview date format"
                }), 400
        else:
            application.interview_date = None

    db.session.commit()

    # Invalidate company dashboard cache so stats stay fresh after any status update
    try:
        cache.delete(f"company_dashboard_{company.id}")
    except Exception:
        pass

    return jsonify({
        "message": "Application updated successfully"
    }), 200


def _send_offer_letter_email(application, job, student, joining_date):
    """Generate a beautiful HTML offer letter and send it to the student."""
    try:
        company = job.company
        joining_str = ""
        if joining_date:
            joining_str = joining_date.strftime("%d %B %Y")
        else:
            joining_str = "To be communicated"
        
        today_str = datetime.utcnow().strftime("%d %B %Y")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Offer Letter - {job.title}</title>
<style>
  body {{ font-family: 'Georgia', serif; background: #f8f9fa; margin: 0; padding: 40px 20px; color: #2d3748; }}
  .container {{ max-width: 700px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.12); }}
  .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%); padding: 40px; text-align: center; }}
  .header h1 {{ color: #ffffff; font-size: 28px; margin: 0 0 4px; font-weight: 700; letter-spacing: 1px; }}
  .header p {{ color: #93c5fd; margin: 0; font-size: 14px; }}
  .body {{ padding: 40px; }}
  .date {{ text-align: right; color: #6b7280; font-size: 14px; margin-bottom: 30px; }}
  .salutation {{ font-size: 18px; font-weight: 600; color: #1e3a8a; margin-bottom: 20px; }}
  p {{ line-height: 1.8; color: #4a5568; margin-bottom: 16px; font-size: 15px; }}
  .highlight-box {{ background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-left: 4px solid #1d4ed8; border-radius: 8px; padding: 20px 24px; margin: 24px 0; }}
  .highlight-box h3 {{ color: #1e3a8a; margin: 0 0 12px; font-size: 16px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }}
  .detail-row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #e0eaff; }}
  .detail-row:last-child {{ border-bottom: none; }}
  .detail-label {{ font-weight: 600; color: #374151; font-size: 13px; }}
  .detail-value {{ color: #1d4ed8; font-weight: 600; font-size: 13px; }}
  .signature {{ margin-top: 40px; padding-top: 30px; border-top: 1px solid #e5e7eb; }}
  .signature p {{ margin: 2px 0; color: #374151; }}
  .company-name {{ font-weight: 700; font-size: 18px; color: #1e3a8a; }}
  .footer {{ background: #f0f7ff; padding: 20px; text-align: center; border-top: 1px solid #dbeafe; }}
  .footer p {{ color: #6b7280; font-size: 12px; margin: 4px 0; }}
  .badge {{ display: inline-block; background: #dcfce7; color: #16a34a; padding: 4px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-bottom: 16px; border: 1px solid #bbf7d0; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🎉 OFFER LETTER</h1>
    <p>Congratulations on your selection!</p>
  </div>
  <div class="body">
    <div class="date">Date: {today_str}</div>
    <div class="salutation">Dear {student.full_name},</div>
    
    <span class="badge">✅ SELECTED</span>
    
    <p>
      We are delighted to inform you that following your recent interview and the subsequent evaluation process, 
      <strong>{company.company_name}</strong> is pleased to offer you the position of 
      <strong>{job.title}</strong> in our organisation.
    </p>
    
    <p>
      We were truly impressed by your academic background, skills, and the enthusiasm you demonstrated throughout the selection process. 
      We believe you will make a significant contribution to our team and we look forward to having you on board.
    </p>

    <div class="highlight-box">
      <h3>📋 Offer Summary</h3>
      <div class="detail-row">
        <span class="detail-label">Position</span>
        <span class="detail-value">{job.title}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Company</span>
        <span class="detail-value">{company.company_name}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Industry</span>
        <span class="detail-value">{company.industry}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Compensation Package</span>
        <span class="detail-value">{job.salary_range}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Date of Joining</span>
        <span class="detail-value">{joining_str}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Location</span>
        <span class="detail-value">{company.location}</span>
      </div>
    </div>

    <p>
      You are requested to report to our office / remote setup on your joining date with the required documents. 
      Further details regarding your onboarding process, documentation, and team introduction will be shared with you closer to the joining date.
    </p>

    <p>
      Please confirm your acceptance of this offer by responding to this email or contacting our HR team within <strong>3 business days</strong> of receipt of this letter.
    </p>

    <p>
      We wish you all the best and sincerely look forward to having you as a valued member of the <strong>{company.company_name}</strong> family.
    </p>

    <div class="signature">
      <p>Warm Regards,</p>
      <p class="company-name">{company.company_name}</p>
      <p style="color: #6b7280; font-size: 13px;">{company.industry} &bull; {company.location}</p>
      {f'<p style="color: #6b7280; font-size: 13px;">{company.website}</p>' if company.website else ''}
    </div>
  </div>
  <div class="footer">
    <p>🎓 This offer letter was generated via <strong>CareerBridge Placement Portal</strong></p>
    <p>For queries, please contact {company.company_name} directly.</p>
  </div>
</div>
</body>
</html>"""

        msg = Message(
            subject=f"🎉 Offer Letter — {job.title} at {company.company_name}",
            recipients=[student.user.email]
        )
        msg.body = f"""Congratulations {student.full_name}!

You have been selected for the position of {job.title} at {company.company_name}.

Compensation: {job.salary_range}
Date of Joining: {joining_str}

Please find your offer letter attached.

Best Regards,
{company.company_name}
"""
        msg.html = html
        mail.send(msg)
    except Exception as e:
        # Don't block the status update if email fails
        print(f"Offer letter email failed: {e}")



@company_bp.route("/application/<int:application_id>/schedule", methods=["POST"])
@jwt_required()
def schedule_interview(application_id):
    company = get_current_company()
    response = validate_company(company) 

    if response:
        return response

    application = (
        Application.query
        .join(JobPosition)
        .filter(
            Application.id == application_id,
            JobPosition.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({"message": "Application not found"}), 404

    data = request.get_json()
    if "interview_date" not in data:
        return jsonify({"message": "interview_date is required"}), 400

    try:
        dt_raw = data["interview_date"]
        # Treat datetime-local value as IST directly (no conversion)
        dt = datetime.fromisoformat(dt_raw.replace('Z', '').split('.')[0])
        application.interview_date = dt
    except ValueError:
        return jsonify({"message": "Invalid date format. Use ISO format."}), 400

    if application.status not in ["applied", "shortlisted", "interview"]:
        return jsonify({"message": "Cannot schedule an interview from the current status."}), 400

    application.status = "interview"
    app_base_url = os.environ.get("APP_BASE_URL", "http://localhost:5173")
    application.interview_link = f"/interview/room/{application.id}"
    db.session.commit()

    student_email = application.student.user.email
    company_email = application.job.company.user.email

    app_base_url = os.environ.get("APP_BASE_URL", "http://localhost:5173")
    try:
        msg = Message("Interview Scheduled",
                      sender=("CareerBridge", os.environ.get("MAIL_DEFAULT_SENDER", "noreply@careerbridge.app")),
                      recipients=[student_email, company_email])
        msg.body = f"An interview has been scheduled for {dt.strftime('%d %b %Y at %I:%M %p')} IST.\nJoin the room here: {app_base_url}{application.interview_link}"
        mail.send(msg)
    except Exception as e:
        print("Failed to send email:", e)

    return jsonify({"message": "Interview scheduled and emails sent successfully.", "link": application.interview_link}), 200