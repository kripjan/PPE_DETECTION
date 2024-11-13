from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import cx_Oracle

# from config import Config
from app.blueprints.auth import auth
from app.blueprints.dashboard import dashboard
from app.blueprints.detection import detection
from app.blueprints.profile import profile
from flask_login import LoginManager
from app.models.company_model import Company

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)  # Load configuration from config.py

    app.secret_key = 'krijan'
    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://ppe:ppe@KRICTUS:1521/XE'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

    except Exception as e:
        print(f"Database connection error: {e}")
        
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login_bp.login' 

    @login_manager.user_loader
    def load_user(company_id):
        return Company.query.get(int(company_id))

    # Register blueprints
    app.register_blueprint(auth) # auth blueprint
    app.register_blueprint(dashboard) # dashboard blueprint
    app.register_blueprint(detection) # detection blueprint
    app.register_blueprint(profile) # profile blueprint
    
    return app