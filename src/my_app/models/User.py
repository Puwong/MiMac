from my_app.foundation import db
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(128), unique=True)
    teams = db.relationship("TeamUserRelationship", back_populates="team", lazy='dynamic')


    def __init__(self, username, email):
        self.username = username
        self.email = email
