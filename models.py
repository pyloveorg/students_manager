__author__ = 'Kamila Urbaniak, Paulina Gralak'

from datetime import *
from flask_login import UserMixin

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Boolean
from sqlalchemy.types import DateTime
from main import bcrypt, db, app
from hashlib import md5
import flask_whooshalchemy as wa
from flask_admin.contrib.sqla import ModelView
from main import admin

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
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), unique=True)


    def __init__(self, username, email, password, admin, confirmed=False,
                 confirmed_on=None, password_reset_token=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.password_reset_token = password_reset_token
        self.registered_on = datetime.utcnow()


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
    index = Column(Integer, unique=True)
    name = Column(String(25), default='')
    surname = Column(String(25), default='')
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user = db.relationship('User', backref='student')

    def __init__(self, index='', name='', surname='', faculty='', major='', year='', group=''):
        self.index = index
        self.name = name
        self.surname = surname
        self.faculty = faculty
        self.major = major
        self.year = year
        self.group = group

    def __repr__(self):
        return "Student(id={}, index={}, name={}, surname={}, faculty={}, year={}, group={}".\
            format(self.id, self.index, self.name, self.surname, self.faculty, self.year, self.group)

#wa.whoosh_index(app, Student)


class Faculty(db.Model):

    __tablename__ = 'faculty'
    __searchable__ = ['name']
    id = Column(Integer, autoincrement=True, primary_key=True, )
    name = Column(String(100), default='')
    major = db.relationship('Major', backref='faculty')
    year = db.relationship('Year', backref='faculty')
    group = db.relationship('Group', backref='faculty')
    student = db.relationship('Student', backref='faculty')

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


class Major(db.Model):

    __tablename__ = 'major'
    __searchable__ = ['name']
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), default='')
    year = db.relationship('Year', backref='major')
    group = db.relationship('Group', backref='major')
    student = db.relationship('Student', backref='major')
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


class Year(db.Model):

    __tablename__ = 'year'
    __searchable__ = ['nr']
    id = Column(Integer, autoincrement=True, primary_key=True)
    nr = Column(String(4), default='')
    group = db.relationship('Group', backref='year')
    student = db.relationship('Student', backref='year')
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=False)
    secretary_id = db.Column(db.Integer, db.ForeignKey('secretary.id'), nullable=False)

    def __init__(self, nr=''):
        self.nr = nr

    def __repr__(self):
        return '{}'.format(self.nr)


class Group(db.Model):

    __tablename__ = 'group'
    __searchable__ = ['subject']
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(10), default='')
    student = db.relationship('Student', backref='group')
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable=False)

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


class Secretary(db.Model):

    __tablename__ = 'secretary'
    __searchable__ = ['name', 'surname']
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(25), default='')
    surname = Column(String(25), default='')
    email = Column(String(200))
    year = db.relationship('Year', backref='secretary')

    def __init__(self, name='', surname='', email=''):
        self.name = name
        self.surname = surname
        self.email = email

    def __repr__(self):
        return "{0} {1}".format(self.name, self.surname)


class Subject(db.Model):

    __tablename__ = 'subject'
    __searchable__ = ['name']
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), default='')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Subject(id={}, name={}".\
            format(self.id, self.name)


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
        return "name={}, surname={}".format(self.name, self.surname)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Faculty, db.session))
admin.add_view(ModelView(Major, db.session))
admin.add_view(ModelView(Year, db.session))
admin.add_view(ModelView(Group, db.session))
admin.add_view(ModelView(Subject, db.session))
admin.add_view(ModelView(Secretary, db.session))