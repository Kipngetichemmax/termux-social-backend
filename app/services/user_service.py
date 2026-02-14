from app.models import User
from app.extensions import db, bcrypt, cache
from app.utils.errors import APIError

class UserService:
    @staticmethod
    def register_user(data):
        """Logic to create a new user."""
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            raise APIError("Missing username, email, or password", status_code=400)

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            raise APIError("Username already taken", status_code=400)
        
        if User.query.filter_by(email=email).first():
            raise APIError("Email already registered", status_code=400)

        # Hash password and save to DB
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @cache.memoize(timeout=300)
    def get_user_profile(self, user_id):
        """Fetch and cache user profile."""
        user = User.query.get(user_id)
        if not user:
            return None
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }

