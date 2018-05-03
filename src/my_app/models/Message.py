import time
from my_app.foundation import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    root_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_uid = db.Column(db.Integer)
    to_uid = db.Column(db.Integer)
    created_at = db.Column(db.Integer, default=time.time)
