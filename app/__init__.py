from flask import Flask, jsonify
from flask_migrate import Migrate
from app.config import config
from app.extensions import db, bcrypt, cache
from app.api.middleware import limiter

migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # Link migrate to app and db
    migrate.init_app(app, db)

    # Import models inside the factory to register them with db
    with app.app_context():
        from app.models import User, Post

    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    from app.api.posts import posts_bp
    from app.api.feed import feed_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')
    app.register_blueprint(feed_bp, url_prefix='/api/feed')

    # Root route for browser
    @app.route("/")
    def home():
        return jsonify({
            "message": "Welcome to Social Network API",
            "available_endpoints": {
                "auth": "/api/auth",
                "users": "/api/users",
                "posts": "/api/posts",
                "feed": "/api/feed"
            }
        })

    # Register error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    from app.utils.errors import APIError

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
