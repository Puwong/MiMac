#! encoding=utf-8
from my_app.foundation import db

class TeamUserRelationship(db.Model):
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    isLeader = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship("User", back_populates="teams")
    team = db.relationship("Team", back_populates="users")
