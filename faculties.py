from main import app

from flask import render_template, redirect
from flask_login import login_required
from models import Major, Faculty


# return all faculties
@app.route('/faculties/', methods=['GET'])
@login_required
def faculties():
    faculties = Faculty.query.all()
    return render_template('faculty/faculties.html', faculties=faculties)


# return faculty with particular id
@app.route('/faculties/<int:id1>', methods=['GET'])
@login_required
def faculty(id1):
    faculty = Faculty.query.filter(Faculty.id == id1).first()
    return render_template('faculty/faculty.html', faculty=faculty)

# add new faculty
@app.route('/faculties/', methods=['POST'])
@login_required
def add_faculty():
    pass


# return all majors with particular faculty
@app.route('/faculties/<int:id1>/majors', methods=['GET'])
@login_required
def majors(id1):
    faculty = Faculty.query.filter(Faculty.id == id1).first()
    majors = Major.query.filter_by(Faculty.major == id1).all()
    return render_template('faculty/majors.html', faculty=faculty, majors=majors)


# return major with particular faculty and id
@app.route('/faculties/<int:id1>/majors/<int:id2>', methods=['GET'])
@login_required
def major(id1, id2):
    faculty = Faculty.query.filter(Faculty.id == id1).first()
    major = Major.query.filter(Faculty.id == id1 and Major.id == id2).first()
    return render_template('faculty/majors.html', major=major, faculty=faculty)


# add new major with particular faculty
@app.route('/faculties/<int:id1>/majors', methods=['POST'])
@login_required
def add_major(id1):
    pass


# return all years with particular faculty and major
@app.route('/faculties/<int:id1>/majors/<int:id2>/years', methods=['GET'])
@login_required
def years(id1, id2):
    majors = Major.query.filter(Faculty.id == id).all()
    return render_template('faculty/years.html', majors=majors)


# return year with particular faculty, major and id
@app.route('/faculties/<int:id1>/majors/<int:id2>/years/<int:id3>', methods=['GET'])
@login_required
def year(id1, id2):
    majors = Major.query.filter(Faculty.id == id).all()
    return render_template('faculty/majors.html', majors=majors)


# add new year with particular faculty and major
@app.route('/faculties/<int:id1>/major/<int:id2>/years', methods=['POST'])
@login_required
def add_years(id1, id2):
    pass


# todo zabezpieczenie przed otwarciem przez studenta, który nie jest z danego wydziału, kierunku, itd.
# może dekorator?

# return all subjects with particular faculty, major and year
@app.route('/faculties/<int:id1>/majors/<int:id2>/years/<int:id3>/subjects', methods=['GET'])
@login_required
def subjects(id1, id2, id3):
    # subjects = Subject.query.filter(Faculty.id == id1 and Major.id == id2 and Year.id == id3).all()
    # return render_template('faculty/subjects.html', subjects=subjects)
    pass


# return subject with particular faculty, major, year and id
@app.route('/faculties/<int:id1>/major/<int:id2>/years/<int:id3>/subjects/<int:id4>', methods=['GET'])
@login_required
def subject(id1, id2, id3, id4):
    # subjects = Subject.query.filter(Faculty.id == id1 and Major.id == id2 and Year.id == id3 and Subject.id == id4).all()
    # return render_template('faculty/subjects.html', subjects=subjects)
    pass


# return all lectures with particular faculty, major and years
@app.route('/faculties/lectures', methods=['GET'])
@login_required
def faculty_lectures():
    pass


# return all lectures with particular faculty, major and years
@app.route('/faculties/<int:id1>/major/<int:id2>/years/<int:id3>/lectures', methods=['GET'])
@login_required
def lectures(id1, id2, id3):
    pass


# return lecture with particular faculty, major, years and id
@app.route('/faculty/<int:id1>/major/<int:id2>/years/<int:id3>/lectures/<int:id4>', methods=['GET'])
@login_required
def lecture(id1, id2, id3, id4):
    pass

# add new lecture with particular faculty, major and years
@app.route('/faculties/<int:id1>/major/<int:id2>/years/<int:id3>/lectures', methods=['POST'])
@login_required
def add_lecture(id1, id2, id3):
    pass


# plan zajęć dla danej grupy
@app.route('/faculty/<int:id1>/major/<int:id2>/year/<int:id3>/group/<int:id4>/plan', methods=['GET', 'POST'])
@login_required
def plan(id1, id2, id3, id4):
    '''

    plan zajec

    '''
# todo model z planem
    #plan =
    return render_template('plan.html', plan=plan)

