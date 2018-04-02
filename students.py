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


@app.route('/students/', methods=['GET'])
@login_required
def students():
    students = Student.query.filter(Student.faculty == current_user.student.faculty).all()
    return render_template('user/students.html', students=students)


@app.route('/students/<int:index>', methods=['GET'])
@login_required
def student(index):
    st = Student.query.filter(Student.index == index).first()
    return render_template('user/profile.html', user=current_user, student=st)


@app.route('/students/<int:index>/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile(index):
    form = EditProfileForm()
    user = User.query.join(Student).filter(Student.index == index).first()
    if form.validate_on_submit(): #validate and request.method == 'POST'
        user.username = form.username.data
        user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect('students/<int:index>/edit_profile')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', form=form)


@app.route('/students/<int:index>/delete_account', methods=['GET','POST'])
@login_required
def delete_account(index):
    form = DeleteForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.join(Student).filter(Student.index == index).first()
        student = Student.query.join(User).filter(user.id == Student.user_id).first()
        #todo metoda is_correct
        if bcrypt.check_password_hash(user.password, password) is True:
            logout_user()
            db.session.delete(user)
            db.session.delete(student)
            db.session.commit()
            return redirect('/')
    return render_template('user/delete_account.html', form=form)


@app.route('/plan', methods=['GET', 'POST'])
@login_required
def plan():
    '''

    plan zajec

    '''
    return render_template('plan.html')


#todo login with fb & twitter
#todo forgot password
#todo szukaj
#todo chat