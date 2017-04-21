#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    name = StringField(u'管理员名', validators=[Required()])
    password = PasswordField(u'管理员密码', validators=[Required()])
    submit = SubmitField(u'登录')
