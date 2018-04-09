from main import app

from flask import render_template, redirect
from flask_login import login_required
import models

# todo zabezpieczenie przed otwarciem przez studenta, który nie jest z danego wydziału, kierunku, itd.
# może dekorator?

# return all subjects with particular faculty, major and year
@app.route('/faculties/<int:id1>/majors/<int:id2>/years/<int:id3>/groups/<int:id4>/subjects', methods=['GET'])
@login_required
def subjects(id1, id2, id3, id4):
    subjects = models.Subject.query.filter(models.Faculty.id == id1 and models.Major.id == id2
        and models.Year.id == id3 and models.Group.id == id4).all()
    return render_template('faculty/subjects.html', id1=id1, id2=id2, id3=id3, id4=id4, subjects=subjects)


# return subject with particular faculty, major, year and id
@app.route('/faculties/<int:id1>/major/<int:id2>/years/<int:id3>/group/<int:id4>/subjects/<int:id5>', methods=['GET'])
@login_required
def subject(id1, id2, id3, id4, id5):
    # subjects = Subject.query.filter(Faculty.id == id1 and Major.id == id2 and Year.id == id3 and Subject.id == id4).all()
    # return render_template('faculty/subject.html', subjects=subjects)

    pass
