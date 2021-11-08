from __future__ import print_function
from flask import redirect, url_for, render_template, flash, request, session, make_response
from project import app, db, bcrypt
from project.forms import SignInForm, SignUpForm
from project.models import User
from flask_login import current_user, login_user, current_user, logout_user, login_required
from time import time
from datetime import date
import json
import sys
import os

# Get the user database for routes
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

# Protected route for user id and user consumed
@app.route("/protected")
def protected():
    return str(current_user.id)
    return str(current_user.consumed)


# Default route
@app.route("/")
def index():
    db.create_all()
    return render_template('index.html')

#Home route
@app.route("/home")
def home():
    return render_template('index.html')

#Sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #user bcrypt to hash password
        user = User(fname=form.first_name.data, lname=form.last_name.data, email=form.email.data,
                    password=hash_password, user_perk=250, consumed=0, burned=0, calories=0)
        db.session.add(user)
        db.session.commit()
        flash(f'Thank you for signing up with us', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', title='Register', form=form)


#Sign in route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['id'] = user.id
            session['fname'] = user.fname
            return redirect(url_for('user'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('signin.html', form=form)