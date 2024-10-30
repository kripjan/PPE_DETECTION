# app/auth/__init__.py
from flask import Blueprint

login_bp = Blueprint('login_bp', __name__, static_folder='static', template_folder='templates')
from .main import routes  # Import routes to register them with the blueprint
