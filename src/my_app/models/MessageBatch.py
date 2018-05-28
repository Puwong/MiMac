from my_app.foundation import db


class MessageBatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    from_user_id = db.Column(db.Integer, index=True)
    to_user_id = db.Column(db.Integer, index=True)
    messages = db.relationship("Message", backref="message_batch", lazy='dynamic')
