__author__ = 'Kamila Urbaniak, Paulina Gralak'

from flask.ext.login import UserMixin

#import flask_login

from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
from sqlalchemy.types import DateTime
from main import bcrypt

from main import db

from wtforms import Form, validators, StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField


class User(db.Model, UserMixin):
    """
    User model for reviewers.
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(25), default='')
    active = Column(Boolean, default=True)
    email = Column(String(200), unique=True)
    password = Column(String(200), default='')
    admin = Column(Boolean, default=False)

    def get_id(self):
        return self.id

    def is_active(self):
        """
        Returns if user is active.
        """
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        """
        Returns if user is admin.
        """
        return self.admin

    @staticmethod
    def make_password(self, plaintext):
        return bcrypt.generate_password_hash(plaintext).encode('utf-8')

    def check_password(self, password):
        if not self.password or not password:
            return False
        return bcrypt.check_password_hash(self.password, password).decode('utf-8')

    @classmethod
    def create(self, username, password, **kwargs):
        return User(
            username=username,
            password=User.make_password(password),
            **kwargs
        )

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter(User.username == username).first()
        if user and user.check_password(password):
            return user
        else:
            return False


    def __repr__(self):
        return "User(id={}, email={}, password={}, admin={}".format(self.id, self.email, self.password, self.admin)


class Subjects(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    major = Column(String(25), default='')
    faculty = Column(String(25), default='')

    def __repr__(self):
        return "Subject(id={}, name={}, major={}, faculty={}".format(self.id, self.name, self.major, self.faculty)

class Lecture(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    consult = Column(DateTime())

    def __repr__(self):
        return "Subject(id={}, name={}, major={}, faculty={}".format(self.id, self.name, self.major, self.faculty)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
    #todo moc hasła
    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    #submit = SubmitField('Register')


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=5, max=25)])
    remember_me = BooleanField('Remember Me', [validators.DataRequired()], default=True)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        user = User.authenticate(self.username.data, self.password.data)
        if not user:
            self.username.errors.append('Invalid username or password')
            return False

        return True

#todo login przez username lub email


class ChangePassword(Form):
    password = PasswordField('Password', [validators.InputRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
