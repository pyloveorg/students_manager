from app import app
from flask import render_template
import sqlalchemy

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def page_not_found(error):
    return render_template('errors/403.html'), 403


# @app.errorhandler(sqlalchemy.exc.IntegrityError)
# def unique(e):
#     return render_template('errors/')

