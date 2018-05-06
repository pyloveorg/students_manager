import flask_uploads as u
from main import app
from flask import request, flash, render_template

files = u.UploadSet('files', u.IMAGES)

u.configure_uploads(app, files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'files' in request.files:
        filename = files.save(request.files['photo'])
        flash("Photo saved.")
        return filename
    return render_template('upload.html')