# In your auth blueprint or where your homepage route is
from flask import render_template, redirect, url_for, flash
from flask import Blueprint
from flask_login import login_required
from app.blueprints.dashboard import dashboard

@login_required
@dashboard.route('/home', methods=['GET'])
def home_page():
    return render_template('home_page.html')
