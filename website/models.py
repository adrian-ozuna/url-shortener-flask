from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    links = db.relationship("Link")

class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(10000))
    link = db.Column(db.String(10000))
    randomString = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))