import time
from my_app.foundation import db
from my_app.common.constant import MessageType


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.SmallInteger, default=MessageType.NORMAL)  # normal, yes_or_no, must_reply
    reply_message_id = db.Column(db.Integer)  # None if no one to reply
    from_user_id = db.Column(db.Integer)
    message_batch_id = db.Column(db.Integer, db.ForeignKey('message_batch.id'))

    context = db.Column(db.String(2048))
    readed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Integer, default=time.time)
