from main import app, db, lm

from flask import render_template, redirect, request, flash, url_for,jsonify
from flask_login import login_required, logout_user, login_user, current_user
from forms import LoginForm, RegistrationForm, EditProfileForm, \
    ChangePasswordForm, DeleteForm, SearchForm
from models import User, Student
from my_email import send_email
from tokens import generate_confirmation_token, confirm_token
from main import bcrypt

import json

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