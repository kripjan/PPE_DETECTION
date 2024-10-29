from flask import Flask
from flask_wtf.csrf import CSRFProtect
# from config import Config  # Import your configuration class
from .login_bp_folder import login_bp  # Adjust according to your folder structure

def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)  # Load configuration from config.py

    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    # Register blueprints
    app.register_blueprint(login_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)