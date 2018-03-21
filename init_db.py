__author__ = 'Kamila Urbaniak, Paulina Gralak'

from sqlalchemy import create_engine
from main import db, bcrypt
import models


def db_start():
    create_engine('sqlite:///tmp/students_manager.db', convert_unicode=True)
    db.create_all()
    db.session.commit()
    username = "piotr"
    password = bcrypt.generate_password_hash('pppp1234')
    email = 'piotr@dyba.com.pl'
    admin = True
    user = models.User(username, email, password, admin)
    user.poweruser = True
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    db_start()
