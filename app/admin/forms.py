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
