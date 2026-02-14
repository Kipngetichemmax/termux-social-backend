from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.extensions import bcrypt
from app.models import User
import jwt
import datetime
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = UserService.register_user(data)
    return jsonify({
        "message": "User created successfully",
        "user": {"id": user.id, "username": user.username}
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(username=data.get('username')).first()

    if user and bcrypt.check_password_hash(user.password_hash, data.get('password')):
        # Generate JWT Token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200

    return jsonify({"error": "Invalid username or password"}), 401

