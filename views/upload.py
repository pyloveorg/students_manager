import flask_uploads as u
from app import app
from flask import request, render_template, redirect, flash, url_for, send_from_directory, send_file
import os

files = u.UploadSet('files', u.IMAGES)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOADED_FILES_DEST'] = '/Users/Kamila/PycharmProjects/students_manager/files'
app.config['UPLOAD_FOLDER'] = '/Users/Kamila/PycharmProjects/students_manager/files'
u.configure_uploads(app, files)

PATH = '/Users/Kamila/PycharmProjects/students_manager/files'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def make_tree(path):
    tree = dict(name=os.path.basename(PATH), children=[])
    try:
        lst = os.listdir(PATH)
    except OSError:
        pass

    else:
        for name in lst:
            fn = os.path.join(PATH, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree


@app.route('/notes')
def all_files():
    path = os.path.expanduser(u'~')
    return render_template('dirtree.html', tree=make_tree(path))


@app.route('/notes/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = u.secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('all_files'))
    return render_template('upload.html')


@app.route('/notes/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/files/<filename>')
def red(filename):
    return redirect(url_for('uploaded_file', filename=filename))
