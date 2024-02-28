from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from . import db
from .models import User
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email does not exist.', category='error')
        
    return render_template('login.html')

@auth.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('username', None)
        flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password != confirm_password:
            flash('Passwords do not match.', category='error')
        elif len(username) < 2:
            flash('Username should be at least 2 characters long.', category='error')
        elif len(password) < 8:
            flash('Password should be at least 8 characters long.', category='error')
        elif not re.match(email_regex, email):
            flash('Invalid email format.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            session['username'] = new_user.username
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
        return render_template('signup.html', email=email, username=username)
    return render_template('signup.html')