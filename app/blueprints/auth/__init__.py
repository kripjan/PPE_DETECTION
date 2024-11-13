from flask import Blueprint


auth = Blueprint('auth', __name__,
                 template_folder = 'templates',
                 static_folder = 'static',
                 static_url_path = '/auth/static')

from app.blueprints.auth.routes import *