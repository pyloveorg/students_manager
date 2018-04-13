__author__ = 'Kamila Urbaniak, Paulina Gralak'


from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail
from flask_admin import Admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'plaintext'

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'testflask2@gmail.com',
    MAIL_PASSWORD = 'flask1234',
    MAIL_DEFAULT_SENDER = 'testflask2@gmail.com'
))

mail = Mail(app)

db = SQLAlchemy()
db.app = app
db.init_app(app)
lm = LoginManager()
lm.init_app(app)
bcrypt = Bcrypt(app)
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

admin = Admin(app, name='students_manager', template_mode='bootstrap3')

lm.login_view = "login"
lm.session_protection = "strong"

CLIENT_SECRETS_FILE = "/Users/Kamila/PycharmProjects/students_manager/client_secrets.json"

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'

if __name__ == '__main__':
    from students import *
    from faculties import *
    from user import *
    from subjects import *
    from google_drive import *
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = "super secret key"
    app.run(debug=True, port=5000)
