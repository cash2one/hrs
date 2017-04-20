#coding:utf-8
from flask import render_template, redirect, url_for, request, jsonify
from . import auth
from .. import db
from ..models import User, Hospital, Department, Schedule, Order
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, OrderForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime, timedelta

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
    orders = current_user.orders.order_by('date').all()
    return render_template('auth/index.html', orders=orders)

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
    if form.validate_on_submit():
        department_id = form.department.data
        return redirect(url_for('auth.schedule', department_id=department_id))

    return render_template('auth/order.html', form=form, hospital=hospital)

@auth.route('/order-confirm/<schedule_id>', methods=['GET', 'POST'])
@login_required
def order_confirm(schedule_id):
    schedule = Schedule.query.get(schedule_id)

    if request.method == 'POST':
        order = Order(user_id=current_user.id,
                    doctor_id=schedule.doctor.id,
                    department_id=schedule.doctor.department.id,
                    date=Order.generate_date(schedule.weekday_int),
                    weekday=schedule.weekday,
                    time=schedule.time,
                    state=u'挂号',
                    create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        schedule.limit -= 1
        db.session.add(schedule)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('auth.index'))

    return render_template('auth/order_confirm.html', schedule=schedule)

@auth.route('/schedule/submit-order', methods=['GET'])
@login_required
def submit_order():
    schedule_id = request.args.get('schedule_id')
    schedule = Schedule.query.get(schedule_id)
    order = Order(user_id=current_user.id,
                doctor_id=schedule.doctor.id,
                department_id=schedule.doctor.department.id,
                weekday=schedule.weekday,
                time=schedule.time,
                state=u'挂号',
                create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    schedule.limit -= 1
    db.session.add(schedule)
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('auth.index'))

@auth.route('/cancel-order', methods=['GET'])
@login_required
def cancel_order():
    order_id = request.args.get('order_id')
    order = Order.query.get(order_id)

    db.session.delete(order)
    db.session.commit()
    return u'cancel order success'

@auth.route('/schedule/<department_id>', methods=['GET'])
def schedule(department_id):
    department = Department.query.get(department_id)
    week_date = {}
    current_time = datetime.now() + timedelta(days=1)
    current_weekday = current_time.weekday()
    for i in range(7):
        next_day = current_time + timedelta(days=i)
        week_date[next_day.weekday()] = next_day.strftime('%Y-%m-%d')
    week_date['current_time'] = current_time
    week_date['current_weekday'] = current_weekday

    return render_template('auth/schedule.html', department=department, week_date=week_date)

@auth.route('/show-doctor', methods=['GET', 'POST'])
def show_doctor():
    week_time = request.args.get('week_time')
    department_id, weekday, time = week_time.split(',')
    department = Department.query.get(department_id)
    doctors = department.doctors.all()
    schedules = []
    for doctor in doctors:
        schedule = doctor.schedules.filter_by(weekday=weekday, time=time).first()
        if schedule:
            schedules.append(schedule)
    return render_template('doctor_info.html', schedules=schedules)
