# In your auth blueprint or where your homepage route is
from flask import render_template, redirect, url_for, flash
from flask import Blueprint

dashboard = Blueprint('dashboard', __name__,
                      template_folder = 'templates',
                      static_folder = 'static',
                      static_url_path = '/dashboard/static')

@dashboard.route('/home', methods=['GET'])
def homepage():
    return render_template('home_page.html')
