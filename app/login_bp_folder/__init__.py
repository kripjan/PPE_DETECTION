# app/auth/__init__.py
from flask import Blueprint

login_bp = Blueprint('login_bp', __name__, template_folder='templates', static_folder='static')
from .main import routes  # Import routes to register them with the blueprint


#mathi ko login_bp variable banako lai aba jata bata ni access garna milcha ani organize garna sajilo vayo aba

#4th line ma blueprint('') vanney constructor cha jalse    variable = object from bluepront class 