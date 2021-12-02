from __future__ import print_function
from pyexpat import model
from flask import redirect, url_for, render_template, flash, request, session, make_response
from project import app, db, bcrypt
from project.forms import SignInForm, SignUpForm, TextForm
from project.models import User
from flask_login import current_user, login_user, current_user, logout_user, login_required
from time import time
from datetime import date
import json
import sys
import os
from transformers import pipeline
import torch

#Access Alice fine tuned model from huggingface.co
alicew = pipeline('text-generation', model='nlrgroup/Alice_fine_tuned', tokenizer='xlnet-base-cased')
#Access Call of the wild fine tuned model from huggingface.co
wild = pipeline('text-generation', model='CoffeeAddict93/gpt1-call-of-the-wild', tokenizer='openai-gpt')
#Access Sherlockhome fine tuned model from huggingface.co
sherlock = pipeline('text-generation', model='MisterFavourite/Sherlock_Holmes_fine_tuned', tokenizer='gpt2')
output_text = "Result here"
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
    # result = generator(text)[0]['generated_text']
    # print(result)
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

#Route of Alice fine tune model
@app.route('/alice')
def alice():
    return render_template('xlnet_base_cased.html', output_text=output_text)

#Route of Alice fine tune model's result
@app.route('/aft', methods=['GET', 'POST'])
def aft():
    text = request.form['a']
    output_text = alicew(text, max_length=200)[0]['generated_text']
    return render_template('xlnet_base_cased.html', output_text=output_text)

#Route of Call of the wild
@app.route('/gpt1')
def gpt1():
    return render_template('gpt1.html', output_text=output_text)

#Route of Call of the wild model's result
@app.route('/cotw', methods=['GET', 'POST'])
def cotw():
    text = request.form['b']
    output_text = wild(text, max_length=200)[0]['generated_text']
    return render_template('gpt1.html', output_text=output_text)

#Route of Call of the wild
@app.route('/gpt2')
def gpt2():
    return render_template('gpt2.html', output_text=output_text)

#Route of Call of the wild model's result
@app.route('/sherlock', methods=['GET', 'POST'])
def sherlockhome():
    text = request.form['c']
    output_text = sherlock(text, max_length=200)[0]['generated_text']
    return render_template('gpt2.html', output_text=output_text)