from flask import render_template, redirect, url_for
from . import main
from .. import db
from ..models import User, Hospital

@main.route('/', methods=['GET', 'POST'])
def index():
    hospitals = Hospital.query.all()
    return render_template('index.html', hospitals=hospitals)
