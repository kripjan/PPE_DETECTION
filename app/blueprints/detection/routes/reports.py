# In your auth blueprint or where your report route is
from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.blueprints.detection import detection


@detection.route('/reports', methods=['GET'])
@login_required
def reports():
    return render_template('reports_page.html')

