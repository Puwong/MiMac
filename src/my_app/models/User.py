from my_app.foundation import db
from my_app.common.constant import UserRole
from flask.ext.login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy
from .AlgUserRelationship import AlgUserRelationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(128))
    role = db.Column(db.SmallInteger, default=UserRole.NORMAL)

    delete = db.Column(db.Boolean, nullable=False, default=False)
    pending = db.Column(db.Boolean, nullable=False, default=False)

    articles = db.relationship("Article", backref="user", lazy='dynamic')
    algs = db.relationship('AlgUserRelationship', backref='user', lazy='dynamic')
    teams = db.relationship("TeamUserRelationship", backref="user", lazy='dynamic')
    my_teams = db.relationship("Team", backref="owner", lazy='dynamic')
    images = db.relationship("ImageUserRelationship", backref="user", lazy='dynamic')
    image_list = association_proxy('images', 'image')

    def check_password(self, raw):
        if not self.password:
            return False
        return raw == self.password
