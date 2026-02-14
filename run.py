import os
from app import create_app

# Get config name from environment or default to 'development'
config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # On Termux, using 0.0.0.0 allows you to access the app 
    # from your phone's browser or other devices on the same Wi-Fi.
    app.run(
        host='0.0.0.0', 
        port=int(os.getenv('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )

