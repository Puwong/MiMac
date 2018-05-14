# -*- coding: utf-8 -*-

from my_app.foundation import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    uri = db.Column(db.String(128))
    users = db.relationship("FileUserRelationship", back_populates="file", lazy='dynamic')
