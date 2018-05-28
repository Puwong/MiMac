#! encoding=utf-8
from my_app.foundation import db


class ImageUserRelationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    isOwner = db.Column(db.Boolean, nullable=False, default=False)