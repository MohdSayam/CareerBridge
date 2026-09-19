from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from datetime import datetime, timedelta
import random
import re
import os
import urllib.parse
from flask_mail import Message
from app.mail import mail

from app.models import db, User, Student, Company

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)

def is_strong_password(password):
    # Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(regex, password)

def generate_otp():
    return str(random.randint(100000, 999999))


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = data.get("role")

    if not email or not password or not name or not role:
        return jsonify({"message": "Missing Data"}), 400
        
    if role not in ["student", "company"]:
        return jsonify({"message": "Invalid role"}), 400

    if not is_strong_password(password):
        return jsonify({"message": "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character."}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        if existing_user.is_verified:
            return jsonify({"message": "Email already registered"}), 400
        else:
            # User started registration but never verified. Overwrite their unverified account.
            if existing_user.role == "student" and existing_user.student:
                db.session.delete(existing_user.student)
            elif existing_user.role == "company" and existing_user.company:
                db.session.delete(existing_user.company)
            db.session.delete(existing_user)
            db.session.commit()

    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)

    new_user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        is_verified=False,
        otp_code=otp,
        otp_expiry=otp_expiry
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()

        if role == "student":
            new_student = Student(
                user_id=new_user.id,
                full_name=name,
                education="",
                branch="",
                cgpa=0.0,
                graduation_year=0,
                skills="",
                resume_path="",
                profile_picture_url=f"https://ui-avatars.com/api/?name={urllib.parse.quote_plus(name)}&background=random"
            )
            db.session.add(new_student)
        else:
            new_company = Company(
                user_id=new_user.id,
                company_name=name,
                description="",
                industry="",
                website="",
                location="",
                profile_picture_url=f"https://ui-avatars.com/api/?name={urllib.parse.quote_plus(name)}&background=random"
            )
            db.session.add(new_company)

        db.session.commit()
        
        from app.tasks import send_otp_email_task
        send_otp_email_task.delay(email, otp)

        return jsonify({"message": "Registration successful. Please check your email for OTP verification."}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Registration failed", "error": str(e)}), 500
    
@auth_bp.route("/verify-email", methods=["POST"])
def verify_email():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    if user.is_verified:
        return jsonify({"message": "Email is already verified"}), 400
        
    if user.otp_code != otp or datetime.utcnow() > user.otp_expiry:
        return jsonify({"message": "Invalid or expired OTP"}), 400
        
    user.is_verified = True
    user.otp_code = None
    user.otp_expiry = None
    db.session.commit()
    
    return jsonify({"message": "Email verified successfully"}), 200

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "both email and password must present"}), 400
    
    user_exists = User.query.filter_by(email=email).first()
    if not user_exists or not check_password_hash(user_exists.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    if not user_exists.is_verified:
        return jsonify({"message": "Please verify your email before logging in", "is_verified": False}), 403

    if not user_exists.is_active:
        return jsonify({"message": "Account is deactivated"}), 403
    
    access_token = create_access_token(
        identity = str(user_exists.id)
    )

    profile_complete = True
    if user_exists.role == "student" and user_exists.student:
        if user_exists.student.education == "" or user_exists.student.branch == "":
            profile_complete = False
    elif user_exists.role == "company" and user_exists.company:
        if user_exists.company.industry == "" or user_exists.company.location == "":
            profile_complete = False

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "role": user_exists.role,
        "profile_complete": profile_complete
    }), 200

@auth_bp.route("/google/login", methods=["POST"])
def google_login():
    data = request.get_json()
    token = data.get("token")
    role = data.get("role")

    if not token:
        return jsonify({"message": "No credential token provided"}), 400

    try:
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            os.environ.get("GOOGLE_CLIENT_ID")
        )
        email = idinfo["email"]

        user_exists = User.query.filter_by(email=email).first()
        
        if not user_exists:
            if not role:
                role = "student"
            
            if role not in ["student", "company"]:
                return jsonify({"message": "Invalid role"}), 400

            random_password = os.urandom(24).hex()
            hashed_password = generate_password_hash(random_password)

            user_exists = User(
                email=email,
                password_hash=hashed_password,
                role=role,
                is_active=True,
                is_verified=True
            )
            db.session.add(user_exists)
            
            if role == "student":
                picture = idinfo.get("picture")
                if not picture:
                    pic_name = idinfo.get("name", "Unknown User")
                    picture = f"https://ui-avatars.com/api/?name={urllib.parse.quote_plus(pic_name)}&background=random"

                student = Student(
                    user=user_exists,
                    full_name=idinfo.get("name", "Unknown User"),
                    education="",
                    branch="",
                    cgpa=0.0,
                    graduation_year=0,
                    skills="",
                    resume_path="",
                    profile_picture_url=picture
                )
                db.session.add(student)
            else:
                picture = idinfo.get("picture")
                if not picture:
                    pic_name = idinfo.get("name", "Unknown Company")
                    picture = f"https://ui-avatars.com/api/?name={urllib.parse.quote_plus(pic_name)}&background=random"

                company = Company(
                    user=user_exists,
                    company_name=idinfo.get("name", "Unknown Company"),
                    description="",
                    industry="",
                    website="",
                    location="",
                    profile_picture_url=picture
                )
                db.session.add(company)
            db.session.commit()

        if not user_exists.is_active:
            return jsonify({"message": "Account is deactivated"}), 403

        access_token = create_access_token(
            identity = str(user_exists.id)
        )

        profile_complete = True
        if user_exists.role == "student" and user_exists.student:
            if user_exists.student.education == "" or user_exists.student.branch == "":
                profile_complete = False
        elif user_exists.role == "company" and user_exists.company:
            if user_exists.company.industry == "" or user_exists.company.location == "":
                profile_complete = False

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "role": user_exists.role,
            "profile_complete": profile_complete
        }), 200

    except ValueError:
        return jsonify({"message": "Invalid Google token"}), 401
