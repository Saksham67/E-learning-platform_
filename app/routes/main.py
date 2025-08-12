from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin/dashboard.html')
    else:
        return render_template('user/dashboard.html')
