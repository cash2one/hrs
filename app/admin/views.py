#coding:utf-8
from flask_admin.contrib.sqla import ModelView
from .. import models

class UserView(ModelView):
    can_create = False
    column_exclude_list = ['password_hash', ]
    column_searchable_list = ['name', 'phone', 'id_card_number']
    form_excluded_columns = ['password_hash']
    form_args = {
        'name': {
            'label': u'姓名',
        }
    }
    inline_models = (models.Order, )

class ScheduleView(ModelView):
    form_args = {
        'weekday': {
            'label': u'星期',
        }
    }
    column_searchable_list = ['doctor_id']
    form_create_rules = ('date','weekday')
