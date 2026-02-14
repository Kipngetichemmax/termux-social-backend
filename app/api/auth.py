from flask import Blueprint, request, jsonify, current_app
from app.services.user_service import UserService
from app.extensions import bcrypt, generate_jwt
from app.models import User

auth_bp = Blueprint("auth_bp", __name__)


# -----------------------
# Register Route
# -----------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400

    # Use your service layer for registration
    user = UserService.register_user(data)
    return jsonify({
        "message": "User created successfully",
        "user": {"id": user.id, "username": user.username}
    }), 201


# -----------------------
# Login Route
# -----------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing credentials"}), 400

    # Lookup user
    user = User.query.filter_by(username=data.get("username")).first()

    if user and bcrypt.check_password_hash(user.password_hash, data.get("password")):
        # Generate JWT using helper
        token = generate_jwt(user.id)

        return jsonify({
            "message": "Login successful",
            "user": {"id": user.id, "username": user.username},
            "token": token
        }), 200

    return jsonify({"error": "Invalid username or password"}), 401
