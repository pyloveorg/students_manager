__author__ = 'Kamila Urbaniak, Paulina Gralak'

from flask.ext.login import UserMixin

#import flask_login

from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean

from main import db

from wtforms import Form, validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField


class User(db.Model, UserMixin):
    """
    User model for reviewers.
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    email = Column(String(200), unique=True)
    password = Column(String(200), default='')
    admin = Column(Boolean, default=False)

    def is_active(self):
        """
        Returns if user is active.
        """
        return self.active

    def is_admin(self):
        """
        Returns if user is admin.
        """
        return self.admin

    def __repr__(self):
        return "User(id={}, email={}, password={}, admin={}".format(self.id, self.email, self.password, self.admin)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=5, max=25)], validators.InputRequired())
    #todo moc hasła
    email = EmailField('Email Address', [validators.Length(min=6, max=35)], validators.Email())
    password = PasswordField('Password', [validators.InputRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=5, max=25)])
    password = StringField('New Password', [validators.Length(min=5, max=25)])
    email = EmailField('Email Address', [validators.Length(min=6, max=35)], validators.Email())

class ChangePassword(Form):
    password = PasswordField('Password', [validators.InputRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
