from flask import Blueprint, render_template, redirect, url_for, session
from .models import User
from . import db
import re

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    """
    Renders the home page.

    If the user is logged in, it retrieves the user's information from the session and renders the home.html template
    with the user's username. If the user is not logged in, it redirects to the login page.

    Returns:
        If the user is logged in, the rendered home.html template with the user's username.
        If the user is not logged in, a redirect to the login page.
    """
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('home.html', username=user.username)
    return redirect(url_for('auth.login'))