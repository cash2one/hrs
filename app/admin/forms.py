#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Length, EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    name = StringField(u'管理员名', validators=[Required()])
    password = PasswordField(u'管理员密码', validators=[Required()])
    submit = SubmitField(u'登录')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原密码', validators=[Required()])
    password = PasswordField(u'设置新密码', validators=[Required()])
    confirm = PasswordField(u'确认新密码', validators=[Required(), EqualTo('password', message=u'两次密码不相同')])
    submit = SubmitField(u'确认修改')

class DoctorForm(FlaskForm):
    name = StringField(u'名字', validators=[Required()])
    rank = StringField(u'级别', validators=[Required()])
    submit = SubmitField(u'确认')

class DepartmentForm(FlaskForm):
    name = StringField(u'科室名', validators=[Required()])
    intro = StringField(u'简介', validators=[Required()])
    hospital = StringField()
    submit = SubmitField(u'确认')

class HospitalForm(FlaskForm):
    name = StringField(u'医院名', validators=[Required()])
    intro = StringField(u'简介', validators=[Required()])
    addr = StringField(u'地址', validators=[Required()])
    phone = StringField(u'咨询电话', validators=[Required()])
    # notice = StringField(u'通知', validators=[Required()])
    # period = StringField(u'周期', validators=[Required()])
    submit = SubmitField(u'确认')

class RegistrationForm(FlaskForm):
    date = StringField(u'日期', validators=[Required()])
    time = StringField(u'时间', validators=[Required()])
    state = StringField(u'状态', validators=[Required()])
    submit = SubmitField(u'确认')

class ScheduleForm(FlaskForm):
    date = StringField(u'日期', validators=[Required()])
    time = StringField(u'时间', validators=[Required()])
    limit = StringField(u'号源', validators=[Required()])
    submit = SubmitField(u'确认')
