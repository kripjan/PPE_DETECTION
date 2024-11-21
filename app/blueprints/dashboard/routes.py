# In your auth blueprint or where your homepage route is
from flask import render_template, redirect, url_for, flash
from flask import Blueprint
from app.blueprints.dashboard import dashboard


@dashboard.route('/home', methods=['GET'])
def home_page():
    return render_template('home_page.html')
