import os
from flask import Flask, send_from_directory
from flask_migrate import Migrate
from app.config import config
from app.extensions import db, bcrypt, cache
from app.api.middleware import limiter
from app.utils.errors import APIError

# Initialize Migrate object
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    # -----------------------
    # Initialize extensions
    # -----------------------
    db.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # -----------------------
    # Import models inside app context
    # -----------------------
    with app.app_context():
        from app import models

    # -----------------------
    # Register blueprints
    # -----------------------
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    from app.api.posts import posts_bp
    from app.api.feed import feed_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')
    app.register_blueprint(feed_bp, url_prefix='/api/feed')

    # -----------------------
    # Register error handlers
    # -----------------------
    register_error_handlers(app)

    # -----------------------
    # Serve frontend files
    # -----------------------
    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

    @app.route("/")
    def serve_index():  # Renamed to avoid conflicts
        return send_from_directory(frontend_dir, "index.html")

    @app.route("/<path:filename>")
    def serve_assets(filename):
        return send_from_directory(frontend_dir, filename)

    return app


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return error.to_dict(), error.status_code

    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
