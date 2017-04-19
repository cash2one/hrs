#coding: utf-8
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from config import config
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
admins = Admin(name=u'后台管理系统', template_mode='bootstrap3')
babel = Babel()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    admins.init_app(app)
    babel.init_app(app)

    import models
    from .admin import views
    admins.add_view(ModelView(models.Order, db.session))
    admins.add_view(views.UserView(models.User, db.session))
    admins.add_view(views.ScheduleView(models.Schedule, db.session))
    admins.add_view(ModelView(models.Doctor, db.session))
    admins.add_view(ModelView(models.Department, db.session))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
