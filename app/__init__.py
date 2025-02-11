from flask import Flask
from flask_socketio import (
    SocketIO,
)  # Flask-SocketIO enables real-time communication between the server and the client.
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from app.config import DevConfig, EmptyDbConfig

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)  # Load configuration from config.py

    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    try:
        db.init_app(app)

    except Exception as e:
        print(f"Database connection error: {e}")

    migrate.init_app(app, db)
    socketio.init_app(app)

    with app.app_context():
        # importing model classes for migrating
        from app.models.company import Company
        from app.models.object import Object
        from app.models.detection import Detection
        from app.models.detection_object import DetectionObject

        from flask_login import LoginManager

        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = "auth.login"

        # user (ie, company) loader function
        @login_manager.user_loader
        def load_user(company_id):
            return Company.query.get(int(company_id))

        # import blueprints
        from app.blueprints.auth import auth
        from app.blueprints.dashboard import dashboard
        from app.blueprints.detection import detection
        from app.blueprints.profile import profile

        # import blueprint routes
        from app.blueprints.auth import routes
        from app.blueprints.dashboard import routes
        from app.blueprints.detection import routes
        from app.blueprints.profile import routes

        # Register blueprints
        app.register_blueprint(auth, url_prefix="/auth")  # auth blueprint
        app.register_blueprint(dashboard, url_prefix="/dashboard")  # dashboardblueprint
        app.register_blueprint(
            detection, url_prefix="/detection"
        )  # detection blueprint
        app.register_blueprint(profile)  # profile blueprint

    return app
