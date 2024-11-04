# In your auth blueprint or where your login route is
from flask import render_template, redirect, url_for, flash
# from .forms import LoginForm
from .. import camerafeed_bp

@camerafeed_bp.route('/camerafeed', methods=['GET'])
def show_camerafeed():
    return render_template('camerafeed_page.html')
