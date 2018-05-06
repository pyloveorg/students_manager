from main import app, db, lm

from flask import render_template, redirect, request, flash, url_for,jsonify
from flask_login import login_required, logout_user, login_user, current_user
from forms import LoginForm, RegistrationForm, ChangePasswordForm
from models import User, Student
from my_email import send_email
from tokens import generate_confirmation_token, confirm_token
from main import bcrypt
import urllib.request as urllib2

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
    return redirect('/home_page')

@app.route('/home_page', methods=['GET', 'POST'])
def home_page():
    return render_template('home_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        student = Student(
            index=form.index.data,
            name=form.name.data,
            surname=form.surname.data,
            faculty=form.faculty.data,
            major=form.major.data,
            year=form.year.data,
            group=form.group.data,
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            confirmed=False,
            admin=False
        )
        db.session.add(user)
        db.session.add(student)
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
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                flash('Invalid credentials')
                return redirect('/login')
            else:
                if user.is_correct_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    flash('Logged in successfully.')
                    return redirect('/')
    else:
        return render_template('user/login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    current_user.active=False
    logout_user()
    flash('You have been logged out')
    return redirect('/login')


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = current_user
        password = form.password.data
        new_password = form.new_password.data
        if bcrypt.check_password_hash(current_user.password, password):
            user.password = bcrypt.generate_password_hash(new_password)
            db.session.commit()
            flash('Your password has been changed successfully.')
            return redirect('/')
        else:
            flash('Your current password is incorrect.', 'success')
    return render_template('user/change_password.html', form=form)


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    return render_template('calendar.html', date=datetime.utcnow())


@app.route('/data')
def return_data():
    #trzeba podać ścieżkę absolutną, bo u mnie nie działa
    with open('/Users/Kamila/PycharmProjects/students_manager/events', 'r') as file:
        data = json.load(file)
        return jsonify(data)
