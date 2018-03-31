#!/usr/bin/env python
# encoding: utf-8
from main import app, db, lm

from flask import render_template, redirect, request, flash, url_for,jsonify
from flask_login import login_required, logout_user, login_user, current_user
from forms import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm
from models import User, Student
from my_email import send_email
from tokens import generate_confirmation_token, confirm_token

import json

from datetime import *


@lm.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def info():
    print(current_user)
    return render_template('main/info.html')


@app.route('/search', methods=['GET'])
def search():
    pass

@app.route('/students/', methods=['GET'])
@login_required
def students():
    temp = current_user.student
    for i in temp:
        fc = i.faculty
    students = Student.query.filter(Student.faculty == fc).all()
    return render_template('user/students.html', students=students)


@app.route('/students/<int:index>', methods=['GET'])
@login_required
def student(index):
    st = Student.query.filter(Student.index == index).first()
    return render_template('user/profile.html', user=current_user, student=st)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        st = Student(
                index=form.index.data,
                name=form.name.data,
                surname=form.surname.data,
                faculty=form.faculty.data,
                major=form.major.data,
                year=form.year.data,
                group=form.group.data
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            confirmed=False,
            student=[st]
        )
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect('/unconfirmed')

    return render_template('user/register.html', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
        return redirect('/unconfirmed')
    return redirect('/login')

#todo resend

@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('/')
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
            return redirect('/')
        else:
            flash('Invalid credentials')
            return redirect('login')
    return render_template('user/login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    current_user.active=False
    logout_user()
    flash('You have been logged out')
    return redirect('/login')

new_password = ''

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    global new_password
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = current_user
        new_password = form.password.data

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_password', token=token, _external=True)
        html = render_template('user/changed_password.html', username=user.username, confirm_url=confirm_url)
        subject = "Please confirm you want to change your password"
        send_email(user.email, subject, html)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect('/unconfirmed-password')
    return render_template('user/change_password.html', form=form)

@app.route('/confirm-pasword/<token>')
@login_required
def confirm_password(token):
    global new_password
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    user.password = new_password
    db.session.commit()
    flash('Your password has been changed successfully.')
    return redirect('/')


@app.route('/unconfirmed-password')
@login_required
def unconfirmed_password():
    global new_password
    user = current_user
    if user.password != new_password:
        flash('Please confirm your account!', 'warning')
        return render_template('user/unconfirmed_password.html')
    return redirect('/')

@app.route('/students/<int:index>/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile(index):
    form = EditProfileForm()
    if form.validate_on_submit(): #validate and request.method == 'POST'
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect('students/<int:index>/edit_profile')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', form=form)

@app.route('/students/<int:index>/delete_profile', methods=['GET','POST'])
@login_required
def delete_profile(index):
    flash('Are you sure?')
    logout_user()

    return redirect('/')


@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"


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


@app.route('/<int:year>/<string:group>/lectures', methods=['GET'])
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


@app.route('/<int:year>/<string:group>/plan', methods=['GET', 'POST'])
@login_required
def plan():
    '''

    plan zajec

    '''
    return render_template('plan.html')


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    return render_template('calendar.html', date=datetime.utcnow())


@app.route('/data')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')

    #trzeba podać ścieżkę absolutną, bo u mnie nie działa
    with open('/Users/Kamila/PycharmProjects/students_manager/events', 'r') as file:
        data = json.load(file)
        return jsonify(data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


#todo login with fb & twitter
#todo forgot password
#todo szukaj
#todo chat