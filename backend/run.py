from flask import Flask 
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_compress import Compress

from app.models import db, User
from app.cache import cache
from app.mail import mail
from config import config_dict

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

env = os.environ.get("FLASK_ENV", "default")
app.config.from_object(config_dict[env])

db.init_app(app)
cache.init_app(app)
mail.init_app(app)
Compress(app)  # Enable gzip compression on all JSON responses

jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Socket.IO with CORS support
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading", logger=False, engineio_logger=False)

# Register WebRTC signaling handlers
from app.socket_server import register_socket_handlers
register_socket_handlers(socketio)

@app.route("/")
def home():
    return "CareerBridge API is Running"

def create_admin():
    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin_email = os.environ.get("ADMIN_EMAIL")
        admin_password = os.environ.get("ADMIN_PASSWORD")
        
        admin = User(
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            role="admin",
            is_verified=True
        )

        db.session.add(admin)
        db.session.commit()
        print("admin created successfully!")

with app.app_context():
    db.create_all()
    create_admin()

from app.routes.auth_routes import auth_bp
app.register_blueprint(auth_bp)

from app.routes.admin_routes import admin_bp
app.register_blueprint(admin_bp)

from app.routes.student_routes import student_bp
app.register_blueprint(student_bp)

from app.routes.company_routes import company_bp
app.register_blueprint(company_bp)

from app.routes.upload_routes import upload_bp
app.register_blueprint(upload_bp)

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)