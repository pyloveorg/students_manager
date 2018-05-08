__author__ = 'Kamila Urbaniak, Paulina Gralak'

from sqlalchemy import create_engine
from main import db
import models
import json


def db_admin():
    username = "kamila"
    password = "kkkk1234"
    email = 'kamila.urbaniak26@gmail.com'
    user = models.User(username, email, password, admin=True)
    user.poweruser = True
    db.session.add(user)
    db.session.commit()


def db_start():
    create_engine('sqlite:///tmp/students_manager.db', convert_unicode=True)
    db.create_all()
    db.session.commit()
    #db_admin()


if __name__ == '__main__':
    db_start()
