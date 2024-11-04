# app/auth/__init__.py
from flask import Blueprint

monitoring_bp = Blueprint('monitoring_bp', __name__, template_folder='templates', static_folder='static')
from .main import routes  # Import routes to register them with the blueprint