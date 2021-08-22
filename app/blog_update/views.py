from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from .. import db
from flask_login import login_user, logout_user, login_required, current_user
from ..requests import get_db

def index():

    blogs = db.execute(
        'SELECT * FROM blogs'
        'ORDER BY date_created DESC'
    ).fetchall()

def get_post(id, check_author=True):
    thepost = db.execute(
        'SELECT * FROM blogs b JOIN users u ON b.user_id = u.id'
        'WHERE b.id = ?',
        (id,)
    ).fetchone()

    if thepost is None:
        abort(404, f'The post {id} doesn\'t exist')

    if check_author and thepost.user_id != current_user.id:
        abort (403)
    
    return thepost