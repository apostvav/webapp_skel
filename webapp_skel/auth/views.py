from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user

from . import auth
from .forms import LoginForm, SignupForm
from .. import db
from ..models import User


@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('articles.user', username=user.username))
        flash("Incorrect username or password.")
    return render_template("login.html", form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)
