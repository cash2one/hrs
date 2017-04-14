#coding:utf-8
from flask import render_template, redirect, url_for, request
from . import admin
from .. import db
from ..models import Admin, User, Doctor, Department, Hospital, Registration, Schedule
from .forms import LoginForm, ChangePasswordForm, DoctorForm, DepartmentForm, HospitalForm, RegistrationForm, ScheduleForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

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
    return redirect(url_for('admin.login'))

@admin.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template('admin/index.html')
    return redirect(url_for('admin.login'))

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

@admin.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    users = User.query.all()
    return render_template('admin/user.html', users=users)

@admin.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user_id(id):
    user = User.query.get(id)
    return render_template('admin/user.html', users=[user])

@admin.route('/doctor', methods=['GET', 'POST'])
@login_required
def doctor():
    doctors = Doctor.query.all()
    return render_template('admin/doctor.html', doctors=doctors)

@admin.route('/doctor/<int:id>', methods=['GET', 'POST'])
@login_required
def doctor_id(id):
    doctor = Doctor.query.get(id)
    return render_template('admin/doctor.html', doctors=[doctor])

@admin.route('/add-doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    form = DoctorForm()
    departments = Department.query.filter_by(hospital_id=current_user.hospital_id).all()
    if form.validate_on_submit():
        doctor = Doctor(name=form.name.data,
                        rank=form.rank.data,
                        department_id=form.department.data)
        db.session.add(doctor)
        db.session.commit()
        return redirect(url_for('admin.doctor'))
    return render_template('admin/add_doctor.html', form=form, departments=departments)

@admin.route('/department', methods=['GET', 'POST'])
@login_required
def department():
    departments = Department.query.filter_by(hospital_id=current_user.hospital_id).all()
    return render_template('admin/department.html', departments=departments)

@admin.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def department_id(id):
    department = Department.query.get(id)
    return render_template('admin/department.html', departments=[department])

@admin.route('/add-department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                intro=form.intro.data,
                                hospital_id=current_user.hospital_id)
        db.session.add(department)
        db.session.commit()
        return redirect(url_for('admin.department'))
    return render_template('admin/add_department.html', form=form)

@admin.route('/hospital', methods=['GET', 'POST'])
@login_required
def hospital():
    hospitals = Hospital.query.all()
    return render_template('admin/hospital.html', hospitals=hospitals)

@admin.route('/hospital/<int:id>', methods=['GET', 'POST'])
@login_required
def hospital_id(id):
    hospital = Hospital.query.get(id)
    return render_template('admin/hospital.html', hospitals=[hospital])

@admin.route('/add-hospital', methods=['GET', 'POST'])
@login_required
def add_hospital():
    form = HospitalForm()
    if form.validate_on_submit():
        hospital = Hospital(name=form.name.data,
                            intro=form.intro.data,
                            addr=form.addr.data,
                            phone=form.phone.data)
        db.session.add(hospital)
        db.session.commit()
        return redirect(url_for('admin.hospital'))
    return render_template('admin/add_hospital.html', form=form)

@admin.route('/registration', methods=['GET', 'POST'])
@login_required
def registration():
    registrations = Registration.query.all()
    return render_template('admin/registration.html', registrations=registrations)

@admin.route('/registration/<int:id>', methods=['GET', 'POST'])
@login_required
def registration_id(id):
    registration = Registration.query.get(id)
    return render_template('admin/registration.html', registrations=[registration])

@admin.route('/add-registration', methods=['GET', 'POST'])
@login_required
def add_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        registration = Registration(date=form.date.data,
                            time=form.time.data,
                            state=form.state.data,
                            create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(registration)
        db.session.commit()
        return redirect(url_for('admin.registration'))
    return render_template('admin/add_registration.html', form=form)

@admin.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    schedules = Schedule.query.all()
    return render_template('admin/schedule.html', schedules=schedules)

@admin.route('/add-schedule', methods=['GET', 'POST'])
@login_required
def add_schedule():
    form = ScheduleForm()
    doctors = Doctor.query.all()
    if form.validate_on_submit():
        schedule = Schedule(doctor_id=form.doctor.data,
                            date=form.date.data,
                            time=form.time.data,
                            limit=form.limit.data)
        db.session.add(schedule)
        db.session.commit()
        return redirect(url_for('admin.schedule'))
    return render_template('admin/add_schedule.html', form=form, doctors=doctors)
