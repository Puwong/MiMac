#! encoding=utf-8
from my_app.foundation import db


class ImageUserRelationship(db.Model):
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    isOwner = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship("User", back_populates="images")
    image = db.relationship("Image", back_populates="users")
