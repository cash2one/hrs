#coding:utf-8
from flask import render_template, redirect, url_for, request
from . import admin
from .. import db
from ..models import Admin
from .forms import LoginForm, ChangePasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.name.data).first()
        if admin is not None and admin.verify_password(form.password.data):
            login_user(admin, True)
            return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.index'))

@admin.route('/', methods=['GET'])
def index():
    return render_template('admin/index.html')

@admin.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('admin.index'))
    return render_template('admin/change_password.html', form=form)
