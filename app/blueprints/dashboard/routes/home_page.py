# In your auth blueprint or where your homepage route is
from flask import render_template, redirect, url_for, flash
from app.blueprints.dashboard import dashboard


@dashboard.route('/home', methods=['GET'])
def homepage():
    return render_template('home_page.html')
