from wtforms import validators, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField

from flask_wtf import FlaskForm
from wtforms import StringField
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=5, max=25), validators.InputRequired()])
    #todo moc hasła
    email = EmailField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=5, max=25),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
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
