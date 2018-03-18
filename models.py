__author__ = 'Kamila Urbaniak, Paulina Gralak'

from flask_login import UserMixin

from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
from sqlalchemy.types import DateTime
from main import bcrypt, db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


class User(db.Model, UserMixin):

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    """
    User model for reviewers.
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(25), default='', unique=True)
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

    def set_password(self, plaintext_password):
        self.password = bcrypt.generate_password_hash(plaintext_password)

    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    '''def create(self, username, password, **kwargs):
        return User(
            username=username,
            password=User.make_password(self, password),
            **kwargs
        )
        '''

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
