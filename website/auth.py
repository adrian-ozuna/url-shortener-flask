from flask import Blueprint, redirect, render_template, flash, request, get_flashed_messages, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        userEmailChecker = User.query.filter_by(email = email).first()

        if userEmailChecker:
            flash('Email adress already in use.', category="error")
        if len(email) < 3:
            flash("Your email adress must be at least 3 characters long", category="error")
        if len(password) < 8:
            flash("Your password must be at least 8 characters long", category="error")
        if password != passwordConfirm:
            flash("Passwords don't match", category="error")

        messages = get_flashed_messages(with_categories=True)

        if not messages:
            new_user = User(email = email, password = generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            return redirect(url_for("views.dashboard"))
    if not current_user.is_authenticated:
        return render_template("signup.html", user = current_user)
    else:
        return redirect(url_for("views.dashboard"))

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("There's no user associated to that email address.", category="error")
    
    if not current_user.is_authenticated:
        return render_template("login.html", user = current_user)
    else:
        return redirect(url_for("views.dashboard"))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))