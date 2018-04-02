__author__ = 'Kamila Urbaniak, Paulina Gralak'

from datetime import *
from flask_login import UserMixin

import flask.ext.sqlalchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
from sqlalchemy.types import DateTime
from main import bcrypt, db, app
from hashlib import md5
import flask_whooshalchemy as wa
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
    __searchable__ = ['username']
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
    student = db.relationship('Student', backref='user', primaryjoin="User.id ==Student.user_id", uselist=False)

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
    __searchable__ = ['index']
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    index = Column(Integer, unique=True)
    name = Column(String(25), default='')
    surname = Column(String(25), default='')
    year = Column(String(1), default='')
    faculty = db.relationship('Faculty', backref='student', primaryjoin="Student.id == Faculty.student_id", uselist=False)
    secretary = Column(Boolean, default=False)

    def __init__(self, index, name, surname, faculty, secretary=False):
        self.index = index
        self.name = name
        self.surname = surname
        self.faculty = faculty
        self.secretary = secretary

    def is_secretary(self):

        return self.secretary

    def __repr__(self):
        return "Student(id={}, index={}, name={}, surname={}, faculty={}".\
            format(self.id, self.index, self.name, self.surname, self.year, self.faculty)

wa.whoosh_index(app, Student)


class Faculty(db.Model):

    __tablename__ = 'faculty'
    __searchable__ = ['name']
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    major = db.relationship('Major', backref='faculty', primaryjoin="Faculty.id == Major.faculty_id", uselist=False)
    student_id = Column(Integer, ForeignKey('student.id'))

    def __init__(self, name, major):
        self.name = name
        self.major = major

    def __repr__(self):
        return "Faculty(id={}, name={}, major={}".\
            format(self.id, self.name, self.major)


class Major(db.Model):

    __tablename__ = 'major'
    __searchable__ = ['name']
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    year = db.relationship('Year', backref='major', primaryjoin="Major.id == Year.major_id", uselist=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))

    def __init__(self, name, year):
        self.name = name
        self.year = year

    def __repr__(self):
        return "Major(id={}, name={}, year={}".\
            format(self.id, self.name, self.year)


class Year(db.Model):

    __tablename__ = 'year'
    __searchable__ = ['subject']
    id = Column(Integer, autoincrement=True, primary_key=True)
    nr = Column(String(2), default='')
    group = Column(String(2))
    #secretary = db.relationship('Secretary', backref='year', primaryjoin="Year.id == Secretary.year_id", uselist=False)
    #subject = db.relationship('Subject', backref='year', primaryjoin="Year.id == Subject.year_id", uselist=False)
    major_id = Column(Integer, ForeignKey('major.id'))

    # def __init__(self, year, group, secretary='', subject=''):
    def __init__(self, nr, group):
        self.nr = nr
        self.group = group
        # self.secretary = secretary
        # self.subject = subject

    def __repr__(self):
        return "Year(id={},nr={}, group={}". \
            format(self.id, self.nr, self.group)
            #format(self.id, self.group, self.secretary, self.subject)


class Secretary(db.Model):

    __tablename__ = 'secretary'
    __searchable__ = ['name', 'surname']
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    surname = Column(String(25), default='')
    email = Column(String(200))
    year_id = Column(Integer, ForeignKey('year.id'))

    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email

    def __repr__(self):
        return "Secretary(id={}, name={}, surname={}, email={}, ".\
            format(self.id, self.name, self.surname, self.email)


class Subject(db.Model):

    __tablename__ = 'subject'
    __searchable__ = ['name', 'lecture']
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    lecture = db.relationship('Lecture', backref='subject', primaryjoin="Subject.id == Lecture.subject_id")
    year_id =  Column(Integer, ForeignKey('year.id'))

    def __init__(self, name, faculty, major):
        self.name = name
        self.faculty = faculty
        self.major = major

    def __repr__(self):
        return "Subject(id={}, name={}, lecture={}".\
            format(self.id, self.name, self.lecture)


class Lecture(db.Model):

    __tablename__ = 'lecture'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    surname = Column(String(25), default='')
    consult = Column(DateTime)
    subject_id = Column(Integer, ForeignKey('subject.id'))

    def __init__(self, name, surname, consult):
        self.name = name
        self.surname = surname
        self.consult = consult

    def __repr__(self):
        return "Lecture(id={}, name={}, surname={}, consult={}".\
            format(self.id, self.name, self.surname, self.consult)