import os
from flask import send_from_directory
from app import create_app

# Get config name from environment or default to 'development'
config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

# -------------------------------
# Serve frontend HTML (index.html)
# -------------------------------
@app.route("/")
def serve_frontend():
    # Assumes your frontend folder is at the root: ~/social-network/frontend
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    return send_from_directory(frontend_dir, "index.html")

# Serve JS/CSS if needed (optional)
@app.route("/<path:filename>")
def serve_frontend_assets(filename):
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    return send_from_directory(frontend_dir, filename)


if __name__ == '__main__':
    # On Termux, using 0.0.0.0 allows you to access the app
    # from your phone's browser or other devices on the same Wi-Fi.
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
