#!/usr/bin/env python
# encoding: utf-8
from main import app, db, lm

from flask import render_template, redirect, request, flash
from flask_login import login_required, logout_user, current_user
from forms import EditProfileForm, DeleteForm, SearchForm
from models import User, Student
from main import bcrypt


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        data = form.search.data
        results = Student.query.whoosh_search(data).all()
        print(str(results))
        #return redirect('/search_results')
    return render_template('search.html', form=form)


# @app.route('/search_results/<query>', methods=['GET', 'POST'])
# @login_required
# def search_result(query):
#     results = Student.query.whoosh_search(query).all()
#     return render_template('search_results.html', query=query, results=results)

# wszyscy studenci z danego wydziału i kierunku
# todo nawiązywanie kontaktu z danym studentem - mail lub chat
@app.route('/students/', methods=['GET'])
@login_required
def students():
    students = Student.query.filter(Student.faculty == current_user.student.faculty).all()
    return render_template('faculty/students/students.html', students=students)


# profil danego studenta
@app.route('/students/<int:id>', methods=['GET'])
@login_required
def student(id):
    # todo zmienić na user a nie current_user
    user = User.query.filter(Student.id == id).first()
    return render_template('faculty/students/profile.html', user=user)

# zmiana własnego profilu
@app.route('/students/<int:id>/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile(id):
    form = EditProfileForm()
    user = User.query.filter(Student.id == id).first()
    if form.validate_on_submit(): #validate and request.method == 'POST'
        user.username = form.username.data
        user.about_me = form.about_me.data
        #user.student.faculty = form.faculty.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect('students/<int:index>/edit_profile')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('faculty/students/edit_profile.html', form=form, user=user)

# usunięcie własnego konta
@app.route('/students/<int:id>/delete_account', methods=['GET','POST'])
@login_required
def delete_account(id):
    form = DeleteForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.join(Student).filter(Student.id == id).first()
        student = Student.query.join(User).filter(user.id == Student.user_id).first()
        #todo metoda is_correct
        if bcrypt.check_password_hash(user.password, password) is True:
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