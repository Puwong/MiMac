from my_app.foundation import db


class AlgUserRelationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    alg_id = db.Column(db.Integer, db.ForeignKey('alg.id'))
