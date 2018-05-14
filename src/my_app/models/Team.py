from my_app.foundation import db


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    users = db.relationship("TeamUserRelationship", back_populates="team", lazy='dynamic')
