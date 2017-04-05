#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, BooleanField
from wtforms.validators import Required, Length, EqualTo
from wtforms import ValidationError
from wtforms.widgets import Input

class ButtonInput(Input):
    """
    用于显示 input type='button' 式按钮的部件(widget)
    """
    input_type = 'button'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('value', field.label.text)
        return super(ButtonInput, self).__call__(field, **kwargs)


class ButtonField(BooleanField):
    '''
    input type='button'式按钮
    '''
    widget = ButtonInput()


class LoginForm(FlaskForm):
    phone = StringField(u'手机号码', validators=[Required()])
    password = PasswordField(u'登录密码', validators=[Required()])
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    name = StringField(u'姓名', validators=[Required()])
    sex = RadioField(u'性别', choices=[(u'男', u'男'), (u'女', u'女')], validators=[Required()])
    id_card_number = StringField(u'身份证号', validators=[Required()])
    birthday = DateField(u'出生日期', validators=[Required()])
    password = PasswordField(u'设置密码', validators=[Required()])
    confirm = PasswordField(u'确认密码', validators=[Required(), EqualTo('password', message=u'两次密码不相同')])
    phone = StringField(u'手机号码', validators=[Required()])
    verification = StringField(u'手机验证码', validators=[Required()])
    submit = SubmitField(u'注册')
