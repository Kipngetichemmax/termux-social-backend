# app/api/middleware.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # SQLite backend for persistence across restarts
)

# Apply to specific routes
@limiter.limit("5 per minute")
def create_post():
    pass

@limiter.limit("10 per minute")
def login():
    pass
