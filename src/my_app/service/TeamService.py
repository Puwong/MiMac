from flask import g
from .BaseService import BaseService
from .UserService import UserService
from .TeamUserRelationshipService import TeamUserRelationshipService
from my_app.models import Team, TeamUserRelationship
from my_app.common.db_helper import exists_query


class TeamService(BaseService):

    model = Team

    def get_all(self, **kwargs):
        return super(TeamService, self).get_all(**kwargs)

    def create(self, **kwargs):
        owner = UserService(self.db).get(g.user_id)
        team = self.model(**kwargs)
        owner.my_teams.append(team)
        self.db.session.commit()
        return team

    def get_info(self, id_or_ins, with_users=False):
        ins = self.get(id_or_ins)
        info = super(TeamService, self).get_info(ins)
        if with_users:
            users = list()
            for user in ins.users:
                users.append(UserService(self.db).get_info(user.user))
            info.update({
                'users': users,
            })
        return info

    def add_user(self, tid, uid):
        if TeamUserRelationshipService(self.db).get(team_id=tid, user_id=uid):
            return False
        user = UserService(self.db).get(uid)
        if not user:
            return False
        team = self.get(tid)
        rs = TeamUserRelationship()
        rs.team = team
        user.teams.append(rs)
        self.db.session.commit()
        return True

    def del_user(self, tid, uid):
        rs = TeamUserRelationshipService(db).get(team_id=tid, user_id=uid)
        if not rs:
            return False
        self.db.session.delete(rs)
        self.db.session.commit()
        return True
