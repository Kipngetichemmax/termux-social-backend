from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_caching import Cache

# Initialize objects without the app (factory pattern)
db = SQLAlchemy()
bcrypt = Bcrypt()
cache = Cache()

