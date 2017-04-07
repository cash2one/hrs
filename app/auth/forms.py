#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Length, EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    phone = StringField(u'手机号码', validators=[Required()])
    password = PasswordField(u'登录密码', validators=[Required()])
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    name = StringField(u'姓名', validators=[Required()])
    sex = RadioField(u'性别', choices=[(u'男', u'男'), (u'女', u'女')], validators=[Required()])
    id_card_number = StringField(u'身份证号', validators=[Required()])
    birthday = DateField(u'出生日期', validators=[Required()])
    province = StringField()
    city = StringField()
    district = StringField()
    password = PasswordField(u'设置密码', validators=[Required()])
    confirm = PasswordField(u'确认密码', validators=[Required(), EqualTo('password', message=u'两次密码不相同')])
    phone = StringField(u'手机号码', validators=[Required()])
    verification = StringField(u'手机验证码', validators=[Required()])
    submit = SubmitField(u'注册')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原密码', validators=[Required()])
    verification = StringField(u'手机验证码', validators=[Required()])
    password = PasswordField(u'设置新密码', validators=[Required()])
    confirm = PasswordField(u'确认新密码', validators=[Required(), EqualTo('password', message=u'两次密码不相同')])
    submit = SubmitField(u'确认修改')
