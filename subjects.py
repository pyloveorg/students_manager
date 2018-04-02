from main import app

from flask import render_template
from flask_login import login_required, current_user
from models import Subject


@app.route('/<string:faculty>/<string:major>/subjects', methods=['GET'])
@login_required
def subjects():
    temp = current_user.student

    for i in temp:
        fc = i.faculty

    for j in fc:
        mj = j.major

    subjects = Subject.query.filter(Subject.major == mj).all
    return render_template('subjects.html', subjects=subjects)


@app.route('/<string:faculty>/<string:major>/subjects/<string:name>', methods=['GET'])
@login_required
def subject():
    '''

    info o danym przedmiocie:
        prowadzący w zależności od grupy laboratoryjnej
        dni kiedy odbywają się zajęcia
    '''
    pass