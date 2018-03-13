__author__ = 'Kamila Urbaniak, Paulina Gralak'

from sqlalchemy import create_engine
from main import db, bcrypt
import models


def db_start():
    create_engine('sqlite:///tmp/students_manager.db', convert_unicode=True)
    db.create_all()
    db.session.commit()
    user = models.User()
    user.username = "piotr"
    user.password = bcrypt.generate_password_hash('pppp1234')
    user.email = 'piotr@dyba.com.pl'
    user.admin = True
    user.poweruser = True
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    db_start()
