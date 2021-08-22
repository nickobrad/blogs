from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from ..models.user import User
from .forms import LoginForm, RegistrationForm
from ..email import mail_message
from .. import db
from . import authentication

@authentication.route('/', methods = ['GET', 'POST'])
def login():

    title = "Log into Blogs"
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password  = login_form.password.data
        rememberme = login_form.remember.data
        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            login_user(user, rememberme)
            return redirect(request.args.get('next') or url_for('main.home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('authentication.login'))

    return render_template('authentication/login.html', title = title, login_form = login_form)

@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))

@authentication.route('/register', methods = ['GET', 'POST'])
def register():
    title = "Welcome to the family"
    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        firstname = register_form.firstname.data
        secondname = register_form.lastname.data
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        user = User(firstname = firstname, secondname = secondname, username = username, email = email, password = password)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Blogzy", "email/newbie", user.email, user = user)
        return redirect(url_for('authentication.login'))

    return render_template('authentication/register.html', register_form = register_form, title = title)



