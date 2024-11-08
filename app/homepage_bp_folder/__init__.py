# app/auth/__init__.py
from flask import Blueprint

homepage_bp = Blueprint('homepage_bp', __name__, template_folder='templates', static_folder='static')
from .main import routes  # Import routes to register them with the blueprint