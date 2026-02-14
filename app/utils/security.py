# app/utils/security.py
import jwt
from datetime import datetime, timedelta
from flask import current_app

class TokenManager:
    @staticmethod
    def generate_access_token(user_id: int, expires_in: int = 3600) -> str:
        """Generate JWT access token (short-lived)."""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def generate_refresh_token(user_id: int, expires_in: int = 86400 * 30) -> str:
        """Generate refresh token (long-lived, stored in DB)."""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode and verify token."""
        try:
            return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()
