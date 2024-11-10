# In your auth blueprint or where your profile route is
from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from ..import profile_bp


@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile_page.html')
