from my_app import db
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    article = db.relationship(
        'Article', backref=db.backref('person', lazy='joined'), lazy='dynamic')

    def __init__(self, username, email):
        self.username = username
        self.email = email
