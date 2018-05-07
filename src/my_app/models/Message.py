import time
from my_app.foundation import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batck_id = db.Column(db.Integer, db.ForeignKey('message_batch.id'))
    reply_message_id = db.Column(db.Integer)  # self if no one to reply
    from_user_id = db.Column(db.Integer)

    context = db.Column(db.String(20480))

    created_at = db.Column(db.Integer, default=time.time)
