from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from . import db
from .models import User
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle the login functionality.

    If the request method is POST, it checks the provided email and password against the database.
    If the email exists and the password is correct, it sets the user_id and username in the session and redirects to the home page.
    If the email does not exist or the password is incorrect, it displays an appropriate error message.
    If the request method is GET, it renders the login page.

    Returns:
        If the login is successful, it redirects to the home page.
        If the login is unsuccessful or the request method is GET, it renders the login page.
    """
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email does not exist.', category='error')
    if 'user_id' in session:
        return redirect(url_for('views.home'))
    return render_template('login.html')
    

@auth.route('/logout')
def logout():
    """
    Handle the logout functionality.

    If the 'user_id' key exists in the session, it removes the 'user_id' and 'username' keys from the session and displays a success message.
    It then redirects to the login page.

    Returns:
        Redirects to the login page.
    """
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('username', None)
        flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """
    Handle the sign up functionality.

    If the request method is POST, it validates the provided email, username, and password.
    If the email or username already exists in the database, it displays an appropriate error message.
    If the password and confirm password do not match, it displays an error message.
    If the username is less than 2 characters long, it displays an error message.
    If the password is less than 8 characters long, it displays an error message.
    If the email format is invalid, it displays an error message.
    If all the validations pass, it creates a new user, adds it to the database, sets the user_id and username in the session, and redirects to the home page.

    Returns:
        If the sign up is successful, it redirects to the home page.
        If the sign up is unsuccessful or the request method is GET, it renders the sign up page.
    """
    
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
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
        return render_template('signup.html', email=email, username=username)
    if 'user_id' in session:
        return redirect(url_for('views.home'))
    return render_template('signup.html')
    

@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    Handle the profile functionality.

    If the 'user_id' key exists in the session, it retrieves the user from the database.
    If the request method is POST, it performs different actions based on the 'action' parameter.
    If the action is 'edit_name', it renders the profile page with the option to edit the username.
    If the action is 'edit_email', it renders the profile page with the option to edit the email.
    If the action is 'edited_name', it validates and updates the username.
    If the action is 'edited_email', it validates and updates the email.
    If the action is 'delete', it deletes the user account.
    If the 'user_id' key does not exist in the session, it redirects to the login page.

    Returns:
        If the 'user_id' key exists in the session, it renders the profile page.
        If the 'user_id' key does not exist in the session, it redirects to the login page.
    """
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'edit_name':
                return render_template('profile.html', user=user, edit_name=True)
            elif action == 'edit_email':
                return render_template('profile.html', user=user, edit_email=True)
            elif action == 'edited_name':
                new_username = request.form.get('username')
                username_exists = User.query.filter_by(username=new_username).first()
                if username_exists:
                    flash('Username is already in use.', category='error')
                elif len(new_username) < 2:
                    flash('Username should be at least 2 characters long.', category='error')
                else:
                    user.username = new_username
                    db.session.commit()
                    flash('Username updated!', category='success')
                return redirect(url_for('auth.profile'))
            elif action == 'edited_email':
                new_email = request.form.get('email')
                email_exists = User.query.filter_by(email=new_email).first()
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                
                if email_exists:
                    flash('Email is already in use.', category='error')
                elif not re.match(email_regex, new_email):
                    flash('Invalid email format.', category='error')
                else:
                    user.email = new_email
                    db.session.commit()
                    flash('Email updated!', category='success')
                return redirect(url_for('auth.profile'))
            elif action == 'delete':
                db.session.delete(user)
                db.session.commit()
                session.pop('user_id', None)
                flash('Account deleted!', category='success')
                return redirect(url_for('auth.login'))
        else:
            return render_template('profile.html', user=user)
    return redirect(url_for('auth.login'))

@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """
    Handle the change password functionality.

    If the 'user_id' key exists in the session, it retrieves the user from the database.
    If the request method is POST, it checks the old password against the user's password.
    If the old password is correct, it validates and updates the new password.
    If the old password is incorrect, it displays an error message.
    If the 'user_id' key does not exist in the session, it redirects to the login page.

    Returns:
        If the 'user_id' key exists in the session, it renders the change password page.
        If the 'user_id' key does not exist in the session, it redirects to the login page.
    """
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if request.method == 'POST':
            old_password = request.form.get('old-password')
            new_password = request.form.get('new-password')
            confirm_new_password = request.form.get('confirm-new-password')
            if check_password_hash(user.password, old_password):
                if new_password != confirm_new_password:
                    flash('Passwords do not match.', category='error')
                elif len(new_password) < 8:
                    flash('Password should be at least 8 characters long.', category='error')
                else:
                    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                    db.session.commit()
                    flash('Password updated!', category='success')
                    return redirect(url_for('auth.profile'))
            else:
                flash('Incorrect password.', category='error')
        return render_template('change_password.html')
    return redirect(url_for('auth.login'))