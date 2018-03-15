#!/usr/bin/env python
# encoding: utf-8
from main import app
from main import db
from main import bcrypt
from main import lm

from flask import render_template, redirect, request, flash, Blueprint, session
from flask.ext.login import LoginManager, login_required, logout_user, login_user, current_user
from models import User, LoginForm, RegistrationForm
from flask import g

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/', methods=['GET', 'POST'])
def info():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
               "<b><a href = '/logout'>click here to log out</a></b>"
    else:
        return render_template('info.html')

@app.route('/search', methods=['GET'])
def search():
    pass

@app.route('/profile', methods=['GET'])
def profile():
    pass

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
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
                login_user(form.user, remember=form.remember_me.data)
                flash('Logged in successfully.')
                return redirect('/')
    else:
        form = LoginForm()
        return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect('/login')

@app.route('/edit-profile', methods=['GET'])
@login_required
def edit_profile():
    pass

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    pass

@app.route('/subjects', methods=['GET'])
@login_required
def subjects():
    '''

    lista wszystkich przedmiotow odpowiednia dla danego studenta kierunku i roku

    '''
    pass

@app.route('/subjects/<string:name>', methods=['GET'])
@login_required
def subject():
    '''

    info o danym przedmiocie:
        prowadzący w zależności od grupy laboratoryjnej
        dni kiedy odbywają się zajęcia
    '''
    pass

@app.route('/lectures', methods=['GET'])
@login_required
def lectures():
    '''

    lista wszystkich prowadzących odpowiednich dla danego studenta kierunku i roku

    '''
    pass

@app.route('/lectures/<string:name>', methods=['GET'])
@login_required
def lecture():
    '''

    info o danym prowadzącym
        dzien i miejsce konsultacji

    '''
    pass

@app.route('/plan', methods=['GET', 'POST'])
@login_required
def plan():
    pass



#todo remember me
#todo login with fb & twitter
#todo forgot password
#todo szukaj
#todo chat