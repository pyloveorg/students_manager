#!/usr/bin/env python
# encoding: utf-8
from main import app, db
from sqlalchemy import func, or_


from flask import render_template, redirect, request, flash
from flask_login import login_required, logout_user, current_user
from forms import EditProfileForm, DeleteForm, SearchForm
from models import User, Student, Faculty, Major, Subject

'''
whoosh_search
'''
# CHOICES = {'Student': Student,'Faculty': Faculty, 'Major': Major, 'Subject': Subject }
#
# @app.route('/search', methods=['GET', 'POST'])
# @login_required
# def search():
#     form = SearchForm()
#     if form.validate_on_submit():
#         select = form.select.data
#         search = form.search.data
#         return search_result(select, search)
#     return render_template('search.html', form=form)
#
#
# @app.route('/search_results/<query>', methods=['GET', 'POST'])
# @login_required
# def search_result(select, search):
#     qry = CHOICES[select]
#     print(qry.surname)
#     results = qry.query.whoosh_search(search).all()
#     return render_template('search_results.html', results=results)


# @app.route('/search', methods=['GET', 'POST'])
# @login_required
# def _search():
#     form = SearchForm()
#     if form.validate_on_submit():
#         select = form.select.data
#         search = form.search.data
#         return search_result(select, search)
#     return render_template('search.html', form=form)
#
'''
basic search
'''
# CHOICES = {'Student': Student,'Faculty': Faculty, 'Major': Major, 'Subject': Subject }
#
# @app.route('/search_results', methods=['GET', 'POST'])
# @login_required
# def search_result(select, search):
#     results = []
#     qry = CHOICES[select]
#     if select == 'Student':
#         res = search.split(' ')
#         if len(res) == 1:
#             students = qry.query.filter(
#                 or_(func.lower(qry.name) == res[0].lower(), func.lower(qry.surname) == res[0].lower())).all()
#         elif len(res) == 2:
#             students = qry.query.filter(func.lower(qry.name) == res[0].lower() and func.lower(qry.surname) == res[1].lower()).all()
#         results = None
#     elif select == 'Faculty':
#         res = search.split(' ')
#         if len(res) == 1:
#             results = qry.query.filter(
#                 or_(func.lower(qry.name) == res[0].lower(), func.lower(qry.surname) == res[0].lower())).all()
#         elif len(res) == 2:
#             results = qry.query.filter(func.lower(qry.name) == res[0].lower() and func.lower(qry.surname) == res[1].lower()).all()
#         students = None
#
#     else:
#         results = qry.query.filter(func.lower(qry.name) == search.lower()).all()
#         students = None
#
#     if not results and not students:
#         flash('No results found!')
#         return redirect('/search')
#     else:
#         return render_template('search_results.html', students=students, results=results, qry=qry)




# todo wszyscy studenci z danego wydziału i kierunku
# todo nawiązywanie kontaktu z danym studentem - mail lub chat
@app.route('/students/', methods=['GET'])
@login_required
def students():
    students = Student.query.all()
    return render_template('faculty/students/students.html', students=students)


# profil danego studenta
@app.route('/students/<int:id>', methods=['GET'])
@login_required
def student(id):
    student = Student.query.filter(Student.id == id).first()
    user = User.query.filter(User.id == student.id + 1).first()
    return render_template('faculty/students/profile.html', user=user, student=student, current_user=current_user)

# zmiana własnego profilu
@app.route('/students/<int:id>/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile(id):
    form = EditProfileForm()
    user = User.query.filter(Student.id == id).first()
    if form.validate_on_submit(): #validate and request.method == 'POST'
        user.username = form.username.data
        user.about_me = form.about_me.data
        user.student.faculty = form.faculty.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect('students/<int:index>/edit_profile')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('faculty/students/edit_profile.html', form=form, user=user)

# usunięcie konta
# starosta może usuwać konta studentów
@app.route('/students/<int:id>/delete_account', methods=['GET','POST'])
@login_required
def delete_account(id):
    form = DeleteForm()
    if form.validate_on_submit():
        user = User.query.join(Student).filter(Student.id == id).first()
        student = Student.query.join(User).filter(Student.id == id).first()
        if current_user.is_correct_password(form.password.data) is True:
            logout_user()
            db.session.delete(user)
            db.session.delete(student)
            db.session.commit()
            return redirect('/')
    return render_template('user/delete_account.html', form=form)


#todo login with fb & twitter
#todo forgot password
#todo szukaj
#todo chat