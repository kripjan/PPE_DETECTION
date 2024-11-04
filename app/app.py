from flask import Flask
from flask_wtf.csrf import CSRFProtect
import cx_Oracle
# from config import Config
from .login_bp_folder import login_bp
from .signup_bp_folder import signup_bp
from .monitoring_bp_folder import monitoring_bp

def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)  # Load configuration from config.py

    app.secret_key = 'krijan'
    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    try:
        app.config['ORACLE_CONN'] = cx_Oracle.connect(
            user='ppe',
            password='ppe',
            dsn='localhost/XEPDB1'  # DSN of Oracle setup
        )
    except cx_Oracle.DatabaseError as e:
        print(f"Database connection error: {e}")

    # Register blueprints
    app.register_blueprint(login_bp) # login blueprint
    app.register_blueprint(signup_bp) # signup blueprint
    app.register_blueprint(monitoring_bp) # signup blueprint
    
    return app

