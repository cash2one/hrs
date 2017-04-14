#coding:utf-8
from flask import render_template, redirect, url_for, request, jsonify
from . import auth
from .. import db
from ..models import User, Hospital, Department
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, OrderForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime, timedelta

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        phone = request.args.get('phone')
        if phone is not None:
            User.send_msg(phone)

    if form.validate_on_submit():
        if User.verify_code(form.phone.data, form.verification.data):
            addr = form.province.data + form.city.data + form.district.data
            addr = addr.strip()
            user = User(name=form.name.data,
                        sex=form.sex.data,
                        addr=addr,
                        id_card_number=form.id_card_number.data,
                        birthday=form.birthday.data,
                        password=form.password.data,
                        phone=form.phone.data,
                        create_at=date.today().strftime("%Y-%m-%d"))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/index', methods=['GET'])
@login_required
def index():
    hospitals = Hospital.query.all()
    return render_template('auth/index.html', hospitals=hospitals)

@auth.route('/info', methods=['GET'])
@login_required
def info():
    return render_template('auth/info.html')

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'GET':
        phone = request.args.get('phone')
        if phone is not None:
            User.send_msg(phone)

    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data) and current_user.verify_code(current_user.phone, form.verification.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('auth.info'))
    return render_template('auth/change_password.html', form=form)

@auth.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    hospital = Hospital.query.first();
    now = datetime.now()
    week = [now + timedelta(days=i) for i in range(7)]
    if form.validate_on_submit():
        department = Department.query.get(form.department.data)
        # date = form.date.data.strftime('%Y-%m-%d')
        return render_template('auth/schedule.html', department=department, week=week)

    return render_template('auth/order.html', form=form, hospital=hospital)

@auth.route('/schedule/<int:department_id>', methods=['GET'])
def schedule(department_id):
    department = Department.query.get(department_id)
    return render_template('auth/schedule.html', department=department)
