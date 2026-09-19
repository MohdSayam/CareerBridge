from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()
IST = pytz.timezone("Asia/Kolkata")

def now_ist():
    """Return current datetime in IST as a naive datetime (for DB storage)."""
    return datetime.now(IST).replace(tzinfo=None)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=now_ist, nullable=False)

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    education = db.Column(db.Text, nullable=False)
    branch = db.Column(db.String(255), nullable=False)
    cgpa = db.Column(db.Float, nullable=False) 
    graduation_year = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Text)
    skills =db.Column(db.String(255), nullable=False) 
    resume_path = db.Column(db.String(255), nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    profile_picture_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=now_ist, nullable=False)

    user = db.relationship("User", backref=db.backref("student", uselist=False))

class Company(db.Model):
    __tablename__ = "companies"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    company_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    industry = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255))
    location = db.Column(db.Text, nullable=False)
    approval_status = db.Column(db.String(55), nullable=False, default="pending")
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    profile_picture_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=now_ist, nullable=False)

    user = db.relationship("User", backref=db.backref("company", uselist=False))

class JobPosition(db.Model):
    __tablename__ = "job_positions"

    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    salary_range = db.Column(db.String(255), nullable=False)
    skills_required = db.Column(db.Text)
    experience_required = db.Column(db.String(100))
    minimum_cgpa = db.Column(db.Float, nullable=False)
    eligible_branch = db.Column(db.String(255), nullable=False)
    eligible_year = db.Column(db.String(50), nullable=False)  # e.g. "2025" or "2025,2026"
    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(255), default="approved", nullable=False)
    created_at = db.Column(db.DateTime, default=now_ist, nullable=False)

    company = db.relationship("Company", backref=db.backref("job_positions"))

class Application(db.Model):
    __tablename__ = "applications"

    __table_args__ = (
        db.UniqueConstraint("student_id", "job_id", name="unique_student_job")
    ),

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job_positions.id"), nullable=False)
    status = db.Column(db.String(50), default="applied", nullable=False)
    applied_at = db.Column(db.DateTime, default=now_ist, nullable=False)
    feedback = db.Column(db.Text)
    interview_date = db.Column(db.DateTime)
    interview_link = db.Column(db.String(500))
    interview_notes = db.Column(db.Text)

    student = db.relationship("Student", backref=db.backref("applications"))
    job = db.relationship("JobPosition", backref=db.backref("applications"))

class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False, unique=True)
    salary = db.Column(db.String(255), nullable=False)
    joining_date = db.Column(db.DateTime)
    offer_letter_path = db.Column(db.String(255))
    placed_on = db.Column(db.DateTime, default=now_ist, nullable=False)

    application = db.relationship("Application", backref=db.backref("placement", uselist=False))