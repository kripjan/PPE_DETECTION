from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from config.py

    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    try:
        db.init_app(app)

    except Exception as e:
        print(f"Database connection error: {e}")

    # importing model classes for migrating
    from app.models.company_model import Company
    from app.models.camera_model import Camera
    from app.models.frame_model import Frame
    from app.models.object_model import Object
    from app.models.frame_object_model import FrameObject
    
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 

    # user (ie, company) loader function 
    @login_manager.user_loader
    def load_user(company_id):
        return Company.query.get(int(company_id))

    with app.app_context():
        # Register blueprints
        from app.blueprints.auth.routes import auth
        from app.blueprints.dashboard.routes import dashboard
        from app.blueprints.detection import detection
        from app.blueprints.profile import profile

        app.register_blueprint(auth, url_prefix='/auth') # auth blueprint
        app.register_blueprint(dashboard, url_prefix='/dashboard') # dashboard blueprint
        app.register_blueprint(detection, url_prefix='/detection') # detection blueprint
        app.register_blueprint(profile) # profile blueprint
    
    return app