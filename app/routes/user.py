from flask import Blueprint, render_template
from app.models import Course

user_bp = Blueprint('user', __name__)

@user_bp.route('/browse')
def browse():
    courses = Course.query.all()
    return render_template('user/browse.html', courses=courses)
