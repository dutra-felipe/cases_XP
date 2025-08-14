from flask import Blueprint, render_template
from flask_login import login_required
from .auth import admin_required


views_bp = Blueprint('views', __name__)


@views_bp.route('/')
@login_required
def index():
    return render_template('dashboard.html')


@views_bp.route('/login')
def login_page():
    return render_template('login.html')


@views_bp.route('/admin')
@admin_required
def admin_page():
    return render_template('admin.html')


@views_bp.route('/case/<int:case_id>')
def case_detail_page(case_id):
    return render_template('case_detail.html')


@views_bp.route('/user-login')
def user_login_page():
    return render_template('user_login.html')
