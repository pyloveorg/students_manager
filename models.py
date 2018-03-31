__author__ = 'Kamila Urbaniak, Paulina Gralak'

from datetime import *
from flask_login import UserMixin

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
from sqlalchemy.types import DateTime
from main import bcrypt, db
from hashlib import md5
from sqlalchemy.orm import relationship

'''
konto admina:
    mianuje starostow
    usuwa i blokuje userow
    usuwa studentow z grup
'''

'''
konto studenta:
    plan
    prowadzacy zajecia
    oceny
    materialy i notatki
'''


'''
konto starosty grupy:
    tworzenie wydarzen oraz ankiet
    wysyłanie informacji do studentów
'''


class User(db.Model, UserMixin):

    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(25), default='', unique=True)
    active = Column(Boolean, default=True)
    email = Column(String(200), unique=True)
    password = Column(String(200), default='')
    admin = Column(Boolean, default=False)
    confirmed = Column(db.Boolean, nullable=False, default=False)
    confirmed_on = Column(db.DateTime, nullable=True)
    registered_on = Column(db.DateTime, nullable=False)
    about_me = Column(String(140))
    last_seen = Column(DateTime, default=datetime.utcnow)
    student = db.relationship('Student', backref='user')
                              #primaryjoin="User.id ==Student.user_id")

    def __init__(self, username, email, password, student, confirmed=False, admin=False,
                 confirmed_on=None, password_reset_token=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.password_reset_token = password_reset_token
        self.registered_on = datetime.utcnow()
        self.student = student

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

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.\
            format(digest, size)

    def __repr__(self):
        return "User(id={}, email={}, password={}, admin={}".\
            format(self.id, self.email, self.password, self.admin)


class Student(db.Model):

    __tablename__ = 'student'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    index = Column(String(8), unique=True)
    name = Column(String(25), default='')
    surname = Column(String(25), default='')
    year = Column(String(1), default='')
    faculty = Column(String(25), default='')
    major = Column(String(25), default='')
    group = Column(String(2), default='')
    secretary = Column(Boolean, default=False)


    def __init__(self, index, name, surname, faculty, major, year, group, secretary=False):
        self.index = index
        self.name = name
        self.surname = surname
        self.faculty = faculty
        self.major = major
        self.year = year
        self.group = group
        self.secretary = secretary

    def is_secretary(self):

        return self.secretary

    def __repr__(self):
        return "Student(id={}, index={}, name={}, surname={}, faculty={}, major={}, year={}, group={}, secretarty={}".\
            format(self.id, self.index, self.name, self.surname, self.year, self.faculty, self.major,
                   self.group, self.secretary)


# class Group(db.Model):
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     group = Column(String(2), default='')
#     year = Column(Integer)
#     secretary = Student.secretary
#
#     def __init__(self, group, year, secretary):
#         self.group = Student.group
#         self.year = year
#         self.secretary = secretary
#
#     def __repr__(self):
#         return "Group(id={}, group={}, year={}, secretarty={}".\
#             format(self.id, self.group, self.year, self.secretary)


class Subject(db.Model):

    __tablename__ = 'subject'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    faculty = Column(String(25), default='')
    major = Column(String(25), default='')

    def __init__(self, name, faculty, major):
        self.name = name
        self.faculty = faculty
        self.major = major

    def __repr__(self):
        return "Subject(id={}, name={}, faculty={}, major={}".\
            format(self.id, self.name, self.faculty, self.major)


class Lecture(db.Model):

    __tablename__ = 'lecture'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    surname = Column(String(25), default='')
    consult = Column(DateTime)

    def __init__(self, name, surname, consult):
        self.name = name
        self.surname = surname
        self.consult = consult

    def __repr__(self):
        return "Lecture(id={}, name={}, surname={}, consult={}".\
            format(self.id, self.name, self.surname, self.consult)