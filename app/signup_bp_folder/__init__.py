# app/auth/__init__.py
from flask import Blueprint

signup_bp = Blueprint('signup_bp', __name__, template_folder='templates', static_folder='static' , static_url_path='\signup_bp_folder\static')
from .main import routes  # Import routes to register them with the blueprint