#coding:utf-8
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from .forms import LoginForm
from .. import models
from flask_login import login_user, logout_user, current_user
from flask import redirect, url_for

class OrderView(ModelView):
    can_create = False
    column_labels = dict(weekday=u'星期', date=u'日期', time=u'时间', doctor=u'医生',
                    user=u'患者', department=u'科室', state=u'状态', create_at=u'创建时间')
    column_searchable_list = ['date', 'time', 'state', models.User.name,models.Doctor.name,
                            models.Department.name]

class UserView(ModelView):
    can_create = False
    column_exclude_list = ['password_hash', 'birthday', 'create_at']
    column_searchable_list = ['name', 'phone', 'id_card_number']
    column_labels = dict(name=u'姓名', id_card_number=u'身份证号', sex=u'性别', addr=u'住址',
                        phone=u'手机号码')
    form_excluded_columns = ['password_hash', 'create_at', 'orders', 'birthday']


class ScheduleView(ModelView):
    column_exclude_list = ['date']
    column_labels = dict(weekday=u'星期', time=u'时间', limit=u'号源', doctor=u'医生')
    column_searchable_list = [models.Doctor.name, 'weekday', 'time']
    form_excluded_columns = ['date']
    form_choices = {
        'weekday': [
            (u'星期一', u'星期一'),
            (u'星期二', u'星期二'),
            (u'星期三', u'星期三'),
            (u'星期四', u'星期四'),
            (u'星期五', u'星期五'),
            (u'星期六', u'星期六'),
            (u'星期日', u'星期日')
        ],
        'time': [
            (u'上午', u'上午'),
            (u'下午', u'下午'),
            (u'晚上', u'晚上')
        ]
    }

class DoctorView(ModelView):
    column_exclude_list = ['intro']
    column_labels = dict(name=u'姓名', rank=u'职称', intro=u'简介', department=u'科室')
    column_searchable_list = ['name', 'rank', models.Department.name]
    form_excluded_columns = ['schedules', 'orders']

class DepartmentView(ModelView):
    column_exclude_list = ['intro', 'hospital']
    column_labels = dict(name=u'科室', intro=u'简介', phone=u'联系电话', hospital=u'医院')
    column_searchable_list = ['name']
    form_excluded_columns = ['doctors', 'orders']

class HospitalView(ModelView):
    can_create = False
    can_delete = False
    column_exclude_list = ['intro', 'notice', 'period']
    column_labels = dict(name=u'医院', intro=u'简介', phone=u'联系电话', addr=u'地址', notice=u'公告')
    form_excluded_columns = ['departments', 'admins']

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login'))
        return self.render('admin/my_master.html')

    @expose('/login', methods=('GET', 'POST'))
    def login(self):
        form = LoginForm()
        if form.validate_on_submit():
            admin = models.Admin.query.filter_by(name=form.name.data).first()
            if admin is not None and admin.verify_password(form.password.data):
                login_user(admin, True)
                return redirect(url_for('.index'))
        return self.render('admin/login.html', form=form)

    @expose('/logout')
    def logout(self):
        logout_user()
        return redirect(url_for('.index'))
