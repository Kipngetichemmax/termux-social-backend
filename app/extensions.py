from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_caching import Cache
import datetime
import jwt
from flask import current_app

# Initialize objects without the app (factory pattern)
db = SQLAlchemy()
bcrypt = Bcrypt()
cache = Cache()


# -----------------------
# JWT Helper Functions
# -----------------------
def generate_jwt(user_id, expires_in=3600):
    """
    Generate a JWT token for a user.
    :param user_id: The ID of the user
    :param expires_in: Token expiration time in seconds (default: 1 hour)
    :return: JWT token as string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token


def decode_jwt(token):
    """
    Decode a JWT token.
    :param token: JWT token string
    :return: payload dict if valid
    :raises: jwt.ExpiredSignatureError, jwt.InvalidTokenError if invalid
    """
    payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    return payload
