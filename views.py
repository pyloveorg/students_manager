#!/usr/bin/env python
# encoding: utf-8
from main import app
from main import db
from main import bcrypt
from main import lm

from flask import render_template, redirect, request, flash, Blueprint, session
from flask.ext.login import LoginManager, login_required, logout_user, login_user
from models import User, LoginForm, RegistrationForm

@lm.user_loader
def load_user(id):
    return User.get(id)

@app.route('/', methods=['GET', 'POST'])
def info():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href = '/logout'>click here to log out</a></b>"
    else:
        return render_template('info.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect('/login')
    else:
        return render_template('register.html', form=form)

#todo potwierdzenie rejestracji na mailu

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user:
            if login_user(user):
                flash('Logged in successfully.')
                return redirect('/<int:username>')
        else:
            error = 'Invalid username or password.'
    else:
        return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/edit-profile', methods=['GET'])
@login_required
def edit_profile():
    pass

@app.route('/<int:username>', methods=['GET'])
def profile():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href ='/logout'>click here to log out</a></b>"
    else:
        return render_template('login.html')

@app.route('/plan', methods=['GET', 'POST'])
@login_required
def plan():
    pass

#todo remember me
#todo login with fb & twitter
#todo forgot password
