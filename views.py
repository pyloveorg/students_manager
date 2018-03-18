#!/usr/bin/env python
# encoding: utf-8
from main import app
from main import db
from main import bcrypt
from main import lm

from flask import render_template, redirect, request, flash, session, url_for
from flask_login import login_required, logout_user, login_user, current_user
from forms import LoginForm, RegistrationForm
from models import User
from flask import g

@lm.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

@app.before_request
def before_request():
    g.user = current_user

@app.route('/', methods=['GET', 'POST'])
def info():
    return render_template('info.html')

@app.route('/search', methods=['GET'])
def search():
    pass

@app.route('/profile', methods=['GET'])
def profile():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
            return redirect('/')
        else:
            return redirect('/login')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
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