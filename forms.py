from wtforms import validators, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField

from flask_wtf import FlaskForm
from wtforms import StringField


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
    #todo moc hasła
    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=5, max=25),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=5, max=25)])
    remember_me = BooleanField('Remember Me', default=True)

#todo login przez username lub email


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', [validators.InputRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
