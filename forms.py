from wtforms import validators, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField
from models import User, Student, Faculty, Major, Year, Group
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from util.validators import Unique


def faculty_choices():
    """ Return all faculties from database. """
    return Faculty.query.all()


def major_choices():
    """ Return all majors from database. """
    return Major.query.all()


def year_choices():
    """ Return all years from database. """
    return Year.query.all()


def group_choices():
    """ Return all groups from database. """
    return Group.query.all()


class RegistrationForm(FlaskForm):

    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired(), Unique(
            User, User.username,
            message='There is already an account with that username.')])
    #todo moc hasła
    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.Email(), Unique(
            User, User.email,
            message='There is already an account with that email.')])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=5, max=25),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    index = StringField('Index', [validators.Length(min=1, max=8), validators.InputRequired(), Unique(
            Student, Student.index,
            message='There is already an account with that index.')])
    name = StringField('Name', [validators.Length(min=3, max=25), validators.InputRequired()])
    surname = StringField('Surname', [validators.Length(min=3, max=25), validators.InputRequired()])
    faculty = QuerySelectField('Faculty', [validators.DataRequired()], query_factory=faculty_choices)
    #todo wybor kierunku w zaleznosci od wydziału - chyba w js
    major = QuerySelectField('Major', [validators.DataRequired()], query_factory=major_choices)
    year = QuerySelectField('Year', [validators.DataRequired()], query_factory=year_choices)
    group = QuerySelectField('Group', [validators.DataRequired()], query_factory=group_choices)
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):

    username = StringField('Username', [validators.InputRequired(), validators.Length(min=5, max=25)])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=5, max=25)])
    remember_me = BooleanField('Remember Me', default=True)
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):

    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=5, max=25)])
    submit = SubmitField('Submit')

#todo login przez username lub email


class ChangePasswordForm(FlaskForm):

    password = PasswordField('Current password', [validators.InputRequired()])
    new_password = PasswordField('New Password', [validators.InputRequired(), validators.Length(min=5, max=25),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat New Password')
    submit = SubmitField('Submit')


class ForgotPasswordForm(FlaskForm):

    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.Email(message=None)])

    def validate(self):
        initial_validation = super(ForgotPasswordForm, self).validate()
        if not initial_validation:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append("This email is not registered")
            return False
        return True

    button = SubmitField('Forgot password')


class EditProfileForm(FlaskForm):

    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
    about_me = TextAreaField('About me', [validators.Length(min=0, max=140)])
    faculty = QuerySelectField('Faculty', [validators.DataRequired()], query_factory=faculty_choices)
    # todo wybor kierunku w zaleznosci od wydziału - chyba w js
    major = QuerySelectField('Major', [validators.DataRequired()], query_factory=major_choices)
    year = QuerySelectField('Year', [validators.DataRequired()], query_factory=year_choices)
    group = QuerySelectField('Group', [validators.DataRequired()], query_factory=group_choices)
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):

    choices = [('Student', 'Student'), ('Faculty', 'Faculty'), ('Major', 'Major'), ('Subject', 'Subject')]
    select = SelectField('Search', [validators.InputRequired()], choices=choices)
    search = StringField('')
    submit = SubmitField('Submit')