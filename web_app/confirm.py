from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# initializing blueprint
confirm = Blueprint('confirm', __name__)


@confirm.route('/login', methods=['POST', "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Filter all users with this email, return the first result; each user should have one
        user = User.query.filter_by(email=email).first()
        if user:
            # checking is user puts in the correct password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # logs in user and remembers the suer is logged in on the session
                login_user(user, remember=True)
                return redirect(url_for('views.prefer'))
            else:
                flash('Incorrect password, try again.', category='error')
        # if email not found, user does not exist/found
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)


# logout route that redirects user to page asking for user login/sign-up
@confirm.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.access'))


@confirm.route('/sign-up', methods=['POST', "GET"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        # checking if user exists
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than three characters.', category='error')
        elif len(user_name) < 3:
            flash('Username must be at least three characters long', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, user_name=user_name, first_name=first_name,
                            last_name=last_name, password=generate_password_hash(password1, method='pbkdf2:sha256', salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.prefer'))

    return render_template("sign_up.html", user=current_user)
