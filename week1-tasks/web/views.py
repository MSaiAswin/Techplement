from flask import Blueprint, render_template, redirect, url_for, request, session

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('auth.login'))

@views.route('/profile')
def profile():
    return render_template('profile.html')

