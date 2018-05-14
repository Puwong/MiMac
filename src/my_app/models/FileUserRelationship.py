#! encoding=utf-8
from my_app.foundation import db


class FileUserRelationship(db.Model):
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    isOwner = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship("User", back_populates="files")
    file = db.relationship("File", back_populates="users")
