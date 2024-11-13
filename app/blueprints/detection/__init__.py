from flask import Blueprint

detection = Blueprint('detection', __name__,
                      template_folder = 'templates',
                      static_folder = 'static',
                      static_url_path = '/detection/static')

from app.blueprints.detection.routes import *