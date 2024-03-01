from flask import Blueprint, render_template, redirect, url_for,session
from .models import User
from . import db
import re

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('home.html', username=user.username)
    return redirect(url_for('auth.login'))