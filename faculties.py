from main import app

from flask import render_template, redirect
from flask_login import login_required
from models import Subject, Major, Faculty, Year


# wszystkie wydziały
@app.route('/faculties/', methods=['GET'])
@login_required
def faculties():
    faculties = Faculty.query.all()
    return render_template('faculty/faculties.html', faculties=faculties)


# kierunki dla odpowiedniego wydziału
@app.route('/faculties/<int:id>/majors', methods=['GET'])
@login_required
def majors(id):
    majors = Major.query.filter(Faculty.id == id).all()
    return render_template('faculty/faculty.html', majors=majors)


# przedmioty dla danego kierunku
@app.route('/faculties/<int:id1>/majors/<int:id2>/year/<int:id3>/subjects', methods=['GET'])
@login_required
def subjects(id1, id2, id3):
    subjects = Subject.query.filter(Faculty.id == id1 and Major.id == id2 and Year.id == id3).all()
    return render_template('faculty/subjects.html', subjects=subjects)


# info o przedmiocie
@app.route('/faculty/<int:id1>/major/<int:id2>/year/<int:id3>/subjects/<int:id4>', methods=['GET'])
@login_required
def subject(id1, id2, id3, id4):
    '''

    info o danym przedmiocie:
        prowadzący w zależności od grupy laboratoryjnej
        dni kiedy odbywają się zajęcia

    '''
    subjects = Subject.query.filter(Faculty.id == id1 and Major.id == id2 and Year.id == id3 and Subject.id == id4).all()
    return render_template('faculty/subjects.html', subjects=subjects)


#plan zajęć dla danej grupy
@app.route('/faculty/<int:id1>/major/<int:id2>/year/<int:id3>/group/<int:id4>/plan', methods=['GET', 'POST'])
@login_required
def plan(id1,id2,id3,id4):
    '''

    plan zajec

    '''
# todo model z planem
    #plan =
    return render_template('plan.html', plan=plan)


@app.route('/faculties/<int:id1>/majors/<int:id2>/year/<int:id3>/group/<int:id4>/students', methods=['GET'])
@login_required
def redirect_students(id1, id2, id3, id4):
    return redirect('/students')


@app.route('/faculties/<int:id1>/majors/<int:id2>/year/<int:id3>/group/<int:id4>/students/<int:id5>', methods=['GET'])
@login_required
def redirect_student(id1, id2, id3, id4, id5):
    return redirect('/students' + id5)