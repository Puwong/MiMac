from my_app.foundation import db
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(128))

    delete = db.Column(db.Boolean, nullable=False, default=False)
    pending = db.Column(db.Boolean, nullable=False, default=False)

    teams = db.relationship("TeamUserRelationship", back_populates="user", lazy='dynamic')
    images = db.relationship("ImageUserRelationship", back_populates="user", lazy='dynamic')

    def check_password(self, raw):
        if not self.password:
            return False
        return raw == self.password
