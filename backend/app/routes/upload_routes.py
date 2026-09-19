import os
import cloudinary
import cloudinary.uploader
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import db, User, Student, Company

# Cloudinary auto-configures from CLOUDINARY_URL env var
cloudinary.config()

upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_RESUME_EXTENSIONS = {"pdf"}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@upload_bp.route("/image", methods=["POST"])
@jwt_required()
def upload_image():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"message": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({"message": "Invalid file type. Only JPG, PNG, GIF, WEBP allowed."}), 400

    try:
        # Upload directly to Cloudinary from the file stream (no local save)
        result = cloudinary.uploader.upload(
            file,
            folder="careerbridge/avatars",
            public_id=f"avatar_{user_id}",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 400, "height": 400, "crop": "fill", "gravity": "face"},
                {"quality": "auto", "fetch_format": "auto"}
            ]
        )
        file_url = result["secure_url"]

        if user.role == "student" and user.student:
            user.student.profile_picture_url = file_url
            db.session.commit()
        elif user.role == "company" and user.company:
            user.company.profile_picture_url = file_url
            db.session.commit()

        return jsonify({"message": "Profile picture uploaded successfully", "url": file_url}), 200

    except Exception as e:
        return jsonify({"message": "Upload failed", "error": str(e)}), 500


@upload_bp.route("/resume", methods=["POST"])
@jwt_required()
def upload_resume():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"message": "Unauthorized"}), 401

    if user.role != "student":
        return jsonify({"message": "Only students can upload resumes"}), 403

    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if not allowed_file(file.filename, ALLOWED_RESUME_EXTENSIONS):
        return jsonify({"message": "Invalid file type. Only PDF allowed."}), 400

    try:
        # Upload PDF to Cloudinary as raw resource (no local save)
        result = cloudinary.uploader.upload(
            file,
            folder="careerbridge/resumes",
            public_id=f"resume_{user_id}.pdf",
            overwrite=True,
            resource_type="raw"  # raw = non-image files like PDFs
        )
        file_url = result["secure_url"]

        if user.student:
            user.student.resume_path = file_url
            db.session.commit()

        return jsonify({"message": "Resume uploaded successfully", "url": file_url}), 200

    except Exception as e:
        return jsonify({"message": "Upload failed", "error": str(e)}), 500
