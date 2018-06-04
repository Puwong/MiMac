# -*- coding: utf-8 -*-

from my_app.foundation import db
from my_app.common.constant import ImageState


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    uri = db.Column(db.String(128))
    state = db.Column(db.SmallInteger, default=ImageState.WAIT_LABEL)
    freeze = db.Column(db.Boolean, default=False)
    delete = db.Column(db.Boolean, default=False)
    users = db.relationship("ImageUserRelationship", backref="image", lazy='dynamic')
    alg_id = db.Column(db.Integer, db.ForeignKey('alg.id'))

    @property
    def store_uri(self):
        return self.uri + '.raw'
