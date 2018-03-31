from wtforms import validators, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField

from flask_wtf import FlaskForm
from wtforms import StringField
from models import User

FACULTY = [
    ('Wydział Architektury', 'Wydział Architektury'),
    ('Wydział Budownictwa i Inżynierii Środowiska', 'Wydział Budownictwa i Inżynierii Środowiska'),
    ('Wydział Budowy Maszyn i Zarządzania','Wydział Budowy Maszyn i Zarządzania'),
]

MAJOR = {
    'Wydział Architektury' :
        [('ar','Architektura')],
    'Wydział Budownictwa i Inżynierii Środowiska':
        [('bd','Budownictwo'), ('is','Inżynieria Środowiska')],
    'Wydział Budowy Maszyn i Zarządzania':
        [('ib','Inżynieria Biomedyczna'), ('im','Inżynieria Materiałowa')]
}

YEAR = [
    ('1','1'), ('2','2'), ('3','3'), ('4','4')
]

# print(FACULTY[0][1])
# print(MAJOR[FACULTY[0][0]])

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
    faculty = SelectField('Faculty', choices=FACULTY)
    #todo wybor kierunku w zaleznosci od wydziału - chyba w js
    major = SelectField('Major', choices=MAJOR[FACULTY[0][0]])
    year = SelectField('Year', choices=YEAR)
    group = StringField('Group', [validators.Length(min=1, max=6), validators.InputRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=5, max=25)])
    remember_me = BooleanField('Remember Me', default=True)
    submit = SubmitField('Submit')

#todo login przez username lub email


class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', [validators.InputRequired(), validators.Length(min=5, max=25),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat New Password')
    confirm = PasswordField('Repeat Password')
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
    submit = SubmitField('Submit')
