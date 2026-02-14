# app/utils/logging_config.py
import logging
import os
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    """Configure structured logging."""
    
    # Create logs directory
    if not os.path.exists('instance/logs'):
        os.makedirs('instance/logs')
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'instance/logs/app.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s] %(message)s'
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    # Log application startup
    app.logger.info('Social Network API starting...')


# Usage in services
class PostService:
    def create_post(self, author_id, content):
        current_app.logger.info(f'Creating post for user {author_id}')
        # ... business logic
        current_app.logger.debug(f'Post created with ID {post.id}')
