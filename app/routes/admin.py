# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from flask_login import login_required, current_user
# from werkzeug.utils import secure_filename
# import os
# from ..models import db, Course, Subject, Material

# admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# # Restrict access to admin only
# def admin_only(func):
#     from functools import wraps
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         if current_user.role != 'admin':
#             flash("Access denied! Admins only.", "danger")
#             return redirect(url_for('main.dashboard'))
#         return func(*args, **kwargs)
#     return decorated_view

# # Admin Dashboard
# @admin_bp.route('/')
# @login_required
# @admin_only
# def admin_dashboard():
#     return render_template('admin/dashboard.html')

# # Add Course
# @admin_bp.route('/add_course', methods=['GET', 'POST'])
# @login_required
# @admin_only
# def add_course():
#     if request.method == 'POST':
#         name = request.form['name']
#         if Course.query.filter_by(name=name).first():
#             flash("Course already exists!", "danger")
#         else:
#             new_course = Course(name=name)
#             db.session.add(new_course)
#             db.session.commit()
#             flash("Course added successfully!", "success")
#             return redirect(url_for('admin.dashboard'))
#     return render_template('admin/courses.html')

# # Add Subject
# @admin_bp.route('/subjects', methods=['GET', 'POST'])
# @login_required
# @admin_only
# def add_subject():
#     courses = Course.query.all()
#     if request.method == 'POST':
#         name = request.form['name']
#         course_id = request.form['course_id']
#         new_subject = Subject(name=name, course_id=course_id)
#         db.session.add(new_subject)
#         db.session.commit()
#         flash("Subject added successfully!", "success")
#         return redirect(url_for('admin.dashboard'))
#     return render_template('admin/subjects.html', courses=courses)

# # Upload Material
# @admin_bp.route('/uploads', methods=['GET', 'POST'])
# @login_required
# @admin_only
# def upload_material():
#     subjects = Subject.query.all()
#     if request.method == 'POST':
#         subject_id = request.form['subject_id']
#         description = request.form['description']
#         file = request.files['file']

#         if file:
#             filename = secure_filename(file.filename)
#             file_path = os.path.join('app/static/uploads', filename)
#             file.save(file_path)

#             new_material = Material(filename=filename, description=description, subject_id=subject_id)
#             db.session.add(new_material)
#             db.session.commit()

#             flash("Material uploaded successfully!", "success")
#             return redirect(url_for('admin.dashboard'))

#     return render_template('admin/uploads.html', subjects=subjects)
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from ..models import db, Course, Subject, Material
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# -----------------------
# Admin-only decorator
# -----------------------
def admin_only(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Access denied! Admins only.", "danger")
            return redirect(url_for('main.dashboard'))
        return func(*args, **kwargs)
    return decorated_view


# -----------------------
# Admin Dashboard
# -----------------------
@admin_bp.route('/')
@login_required
@admin_only
def admin_dashboard():
    return render_template('admin/dashboard.html')


# -----------------------
# Add Course
# -----------------------
@admin_bp.route('/add_course', methods=['GET', 'POST'])
@login_required
@admin_only
def add_course():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash("Course name is required!", "danger")
        elif Course.query.filter_by(name=name).first():
            flash("Course already exists!", "danger")
        else:
            new_course = Course(name=name)
            db.session.add(new_course)
            db.session.commit()
            flash("Course added successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/courses.html')


# -----------------------
# Add Subject
# -----------------------
@admin_bp.route('/subjects', methods=['GET', 'POST'])
@login_required
@admin_only
def add_subject():
    courses = Course.query.all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        course_id = request.form.get('course_id')

        if not name or not course_id:
            flash("All fields are required!", "danger")
        else:
            new_subject = Subject(name=name, course_id=course_id)
            db.session.add(new_subject)
            db.session.commit()
            flash("Subject added successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/subjects.html', courses=courses)


# -----------------------
# Upload Material
# -----------------------
@admin_bp.route('/uploads', methods=['GET', 'POST'])
@login_required
@admin_only
def upload_material():
    subjects = Subject.query.all()

    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        description = request.form.get('description', '').strip()
        file = request.files.get('file')

        if not subject_id or not file:
            flash("Subject and file are required!", "danger")
        else:
            filename = secure_filename(file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
            os.makedirs(upload_folder, exist_ok=True)  # Ensure folder exists
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            new_material = Material(
                filename=filename,
                description=description,
                subject_id=subject_id
            )
            db.session.add(new_material)
            db.session.commit()

            flash("Material uploaded successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/uploads.html', subjects=subjects)
