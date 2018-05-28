#! encoding=utf-8
from my_app.foundation import db


class TeamUserRelationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    isLeader = db.Column(db.Boolean, nullable=False, default=False)
