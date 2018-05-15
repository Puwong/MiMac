# -*- coding: utf-8 -*-

from my_app.foundation import db
from my_app.common.constant import FileState


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    uri = db.Column(db.String(128))
    state = db.Column(db.SmallInteger, default=FileState.STUCK)
    users = db.relationship("FileUserRelationship", back_populates="file", lazy='dynamic')

