#!/usr/bin/env python
# encoding: utf-8
from main import app
from main import db
from main import bcrypt
from main import lm

from flask import render_template, redirect, request, flash, Blueprint, session
import flask_login
from models import User, LoginForm, RegistrationForm

@app.route('/', methods=['GET', 'POST'])
def info():
    return render_template('info.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect('/login')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/logout', methods=['GET'])
def logout():
    pass

@app.route('/edit-profile', methods=['GET'])
def edit_profile():
    pass

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    pass

#todo remember me
#todo login with fb & twitter
#todo forgot password
