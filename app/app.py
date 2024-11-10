from flask import Flask
from flask_wtf.csrf import CSRFProtect
import cx_Oracle
# from config import Config
from .login_bp_folder import login_bp
from .signup_bp_folder import signup_bp
from .monitoring_bp_folder import monitoring_bp
from .homepage_bp_folder import homepage_bp
from .profile_bp_folder import profile_bp
from database import db
from flask_login import LoginManager
from app.signup_bp_folder.main.models.company_model import Company



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
    app.register_blueprint(login_bp) # login blueprint
    app.register_blueprint(signup_bp) # signup blueprint
    app.register_blueprint(monitoring_bp) # signup blueprint
    app.register_blueprint(homepage_bp) #homepage blueprint
    app.register_blueprint(profile_bp) #homepage blueprint
    
    return app

