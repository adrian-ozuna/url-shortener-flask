from flask import Blueprint, redirect, render_template, request, flash, get_flashed_messages, url_for
from flask_login import current_user, login_required
import urllib3
from .models import Link
from . import db
import random
import string

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", user = current_user)

@views.route('/create-link', methods = ['GET', 'POST'])
@login_required
def create_link():
    if request.method == 'POST':
        name = request.form.get("name")
        description = request.form.get("description")
        link = request.form.get("link")

        if not link[:4] == 'http':
            link = f'http://{request.form.get("link")}'

        # If the request returns a 2xx status code, then the given url is good.
        http = urllib3.PoolManager()
        httpStatus = ""
        try:
            httpStatus = str(http.request('GET', link).status)
        except:
            httpStatus = "bad"

        if len(name) < 1:
            flash("A link name is required", category="error")

        if httpStatus == "bad" or httpStatus != httpStatus[:4] == "2":
            flash(f"The link you entered is not working.", category="error")

        messages = get_flashed_messages(with_categories=True)

        if not messages:
            letters = string.ascii_lowercase
            randomString = ''.join(random.choice(letters) for i in range(10))
            new_link = Link(name = name, description = description, link = link, randomString = randomString, user_id = current_user.id)
            db.session.add(new_link)
            db.session.commit()

            print(httpStatus)

            return redirect(url_for('views.dashboard'))

    return render_template("create-link.html", user = current_user)

@views.route('/<string:randomString>')
def get_specific_link(randomString):
    link = Link.query.filter_by(randomString = randomString).first()
    targetUrl = link.link
    return redirect(targetUrl)

@views.route('/delete/<string:randomString>')
@login_required
def delete_specific_link(randomString):
    link = Link.query.filter_by(randomString = randomString).first()
    if link:
        if link.user_id == current_user.id:
            db.session.delete(link)
            db.session.commit()
        
    return redirect(url_for('views.dashboard'))