from wtforms import validators, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField

from flask_wtf import FlaskForm
from wtforms import StringField
from models import User, Faculty, Major, Year, Group
from wtforms.ext.sqlalchemy.fields import QuerySelectField


def faculty_choices():
    return Faculty.query


def major_choices():
    return Major.query.all()


def year_choices():
    return Year.query.all()


def group_choices():
    return Group.query.all()


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
    #todo moc hasła
    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=5, max=25),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    index = StringField('Index', [validators.Length(min=1, max=8), validators.InputRequired()])
    name = StringField('Name', [validators.Length(min=3, max=25), validators.InputRequired()])
    surname = StringField('Surname', [validators.Length(min=3, max=25), validators.InputRequired()])
    faculty = QuerySelectField('Faculty', [validators.DataRequired()], query_factory=faculty_choices)
    #todo wybor kierunku w zaleznosci od wydziału - chyba w js
    major = QuerySelectField('Major', [validators.DataRequired()], query_factory=major_choices)
    year = QuerySelectField('Year', [validators.DataRequired()], query_factory=year_choices)
    group = QuerySelectField('Group', [validators.DataRequired()], query_factory=group_choices)
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
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

    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
    about_me = TextAreaField('About me', [validators.Length(min=0, max=140)])
    faculty = QuerySelectField('Faculty', [validators.DataRequired()], query_factory=faculty_choices)
    # todo wybor kierunku w zaleznosci od wydziału - chyba w js
    major = QuerySelectField('Major', [validators.DataRequired()], query_factory=major_choices)
    year = QuerySelectField('Year', [validators.DataRequired()], query_factory=year_choices)
    group = QuerySelectField('Group', [validators.DataRequired()], query_factory=group_choices)
    submit = SubmitField('Submit')


# class SearchForm(FlaskForm):
#     search = StringField('Search', [validators.InputRequired()])
#     submit = SubmitField('Submit')