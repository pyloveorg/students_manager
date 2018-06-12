from app import app

from flask import render_template, redirect
from flask_login import login_required
import models


# return all faculties
@app.route('/faculties/', methods=['GET'])
@login_required
def faculties():
    faculties = models.Faculty.query.all()
    return render_template('faculty/faculties.html', faculties=faculties)


# return faculty with particular id
@app.route('/faculties/<int:id1>', methods=['GET'])
@login_required
def faculty(id1):
    faculty = models.Faculty.query.filter(models.Faculty.id == id1).first()
    return render_template('faculty/faculty.html', id=id1, faculty=faculty)

# add new faculty
@app.route('/faculties/', methods=['POST'])
@login_required
def add_faculty():
    pass


# return all majors with particular faculty
@app.route('/faculties/<int:id1>/majors', methods=['GET'])
@login_required
def majors(id1):
    majors = models.Major.query.filter(models.Faculty.id == id1).all()
    return render_template('faculty/majors.html', id1=id1, majors=majors)


# return major with particular faculty and id
@app.route('/faculties/<int:id1>/majors/<int:id2>', methods=['GET'])
@login_required
def major(id1, id2):
    major = models.Major.query.filter(models.Faculty.id == id1 and models.Major.id == id2).first()
    return render_template('faculty/major.html', id1=id1, id2=id2, major=major)


# add new major with particular faculty
@app.route('/faculties/<int:id1>/majors', methods=['POST'])
@login_required
def add_major(id1):
    pass


# return all years with particular faculty and major
@app.route('/faculties/<int:id1>/majors/<int:id2>/years', methods=['GET'])
@login_required
def years(id1, id2):
    years = models.Year.query.filter(
        models.Faculty.id == id1 and models.Major.id == id2).all()
    return render_template('faculty/years.html', id1=id1, id2=id2, years=years)


# return year with particular faculty, major and id
@app.route('/faculties/<int:id1>/majors/<int:id2>/years/<int:id3>', methods=['GET'])
@login_required
def year(id1, id2,id3):
    year = models.Major.query.filter(
        models.Faculty.id == id1 and models.Major.id == id2
        and models.Year.id == id3).first()
    return render_template('faculty/year.html', id1=id1, id2=id2, id3=id3, year=year)


# add new year with particular faculty and major
@app.route('/faculties/<int:id1>/major/<int:id2>/years', methods=['POST'])
@login_required
def add_years(id1, id2):
    pass


# return groups with particular faculty, major and years
@app.route('/faculties/<int:id1>/majors/<int:id2>/years/<int:id3>/groups', methods=['GET'])
@login_required
def groups(id1, id2, id3):
    groups = models.Group.query.filter(
        models.Faculty.id == id1 and models.Major.id == id2
        and models.Year.id == id3).all()
    return render_template('faculty/groups.html', id1=id1, id2=id2, id3=id3, groups=groups)


# return group with particular faculty, major, year and id
@app.route('/faculties/<int:id1>/majors/<int:id2>/years/<int:id3>/groups/<int:id4>', methods=['GET'])
@login_required
def group(id1, id2, id3, id4):
    group = models.Group.query.filter(
        models.Faculty.id == id1 and models.Major.id == id2
        and models.Year.id == id3 and models.Group.id == id4).first()
    return render_template('faculty/group.html', id1=id1, id2=id2, id3=id3, id4 =id4, group=group)


# add new group with particular faculty, major and group
@app.route('/faculties/<int:id1>/major/<int:id2>/years/<int:id3>/groups', methods=['POST'])
@login_required
def add_group(id1, id2, id3):
    pass

# todo zabezpieczenie przed otwarciem przez studenta, który nie jest z danego wydziału, kierunku, itd.
# może dekorator?


# return all lectures with particular faculty, major and years
@app.route('/faculties/lectures', methods=['GET'])
@login_required
def faculty_lectures():
    pass


# return all lectures with particular faculty, major and years
@app.route('/faculties/<int:id1>/major/<int:id2>/years/<int:id3>/group/<int:id4>/lectures', methods=['GET'])
@login_required
def lectures(id1, id2, id3):
    pass


# return lecture with particular faculty, major, years and id
@app.route('/faculty/<int:id1>/major/<int:id2>/years/<int:id3>/group/<int:id4>/lectures/<int:id5>', methods=['GET'])
@login_required
def lecture(id1, id2, id3, id4, id5):
    pass

# add new lecture with particular faculty, major and years
@app.route('/faculties/<int:id1>/major/<int:id2>/years/<int:id3>/group/<int:id4>/lectures', methods=['POST'])
@login_required
def add_lecture(id1, id2, id3, id4):
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
    return render_template('schedule.html', plan=plan)

