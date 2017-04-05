from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

class Permissions:
    USER = 0x01


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    id_card_number = db.Column(db.String(50), unique=True, index=True)
    birthday = db.Column(db.String(20))
    sex = db.Column(db.String(5))
    addr = db.Column(db.String(50))
    phone = db.Column(db.String(20), index=True)
    password_hash = db.Column(db.String(128))
    create_at = db.Column(db.String(20))
    registrations = db.relationship('Registration', backref='user', lazy='dynamic')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.name

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    permissions = db.Column(db.Integer)
    password = db.Column(db.String(128))
    create_at = db.Column(db.String(20))

    def can(self, permissions):
        return (self.permissions & permissions) == permissions

    def __repr__(self):
        return '<Admin %r>' % self.name


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    intro = db.Column(db.Text)
    doctors = db.relationship('Doctor', backref='department', lazy='dynamic')
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    registrations = db.relationship('Registration', backref='department', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Department %r>' % self.name


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    rank = db.Column(db.String(20))
    registrations = db.relationship('Registration', backref='doctor', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='doctor', lazy='dynamic')

    def __repr__(self):
        return '<Doctor %r>' % self.name


class Hospital(db.Model):
    __tablename__ = 'hospitals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    intro = db.Column(db.Text)
    addr = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    period = db.Column(db.String(5))
    notice = db.Column(db.Text)
    departments = db.relationship('Department', backref='hospital', lazy='dynamic')

    def __repr__(self):
        return '<Hospital %r>' % self.name


class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    state = db.Column(db.String(10))
    create_at = db.Column(db.String(20))

    def __repr__(self):
        return '<Registration %r>' % self.create_at


class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    limit = db.Column(db.Integer)

    def __repr__(self):
        return '<Schedule %r>' % self.date
