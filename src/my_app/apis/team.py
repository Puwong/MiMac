# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, render_template, request, g, redirect, url_for
from flask_restful import Api, Resource
from flask_login import login_required

from my_app.service import TeamService, TeamUserRelationshipService, hack_alert
from my_app.foundation import csrf, db

team_bp = Blueprint('Team', __name__)
csrf.exempt(team_bp)
team_api = Api(team_bp)


def permission_check(tid, **kwargs):
    team = TeamService(db).get(tid)
    r = TeamUserRelationshipService(db).get(team_id=team.id, user_id=g.user_id)
    if r:
        return r.isLeader or team.owner.id == g.user_id
    return False


class TeamsAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'teams.html',
            teams=TeamService(db).get_all(),
        ))


class MyTeamsAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'teams.html',
            teams=TeamService(db).get_all(owner_id=g.user_id),
        ))

    @login_required
    def post(self):
        return self.get()


class NewTeamAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'team.html',
            new=True,
        ))

    @login_required
    def post(self):
        title = request.form.get('title')
        desc = request.form.get('desc')
        team = TeamService(db).create(title=title, desc=desc)
        return TeamAPI().get(tid=team.id, op='view')


class TeamAPI(Resource):

    @login_required
    def get(self, tid, op):
        if op == 'edit':
            return current_app.make_response(render_template(
                'team.html',
                team=TeamService(db).get(tid),
                edit=True
            ))
        return current_app.make_response(render_template(
            'team.html',
            team=TeamService(db).get(tid),
            isLeader=permission_check(tid)
        ))

    @hack_alert(permission_check)
    @login_required
    def post(self, tid, op):
        if op == 'view':
            return self.get(tid, op)
        team = TeamService(db).get(tid)
        team.title = request.form.get('title')
        team.desc = request.form.get('desc')
        db.session.commit()
        return self.get(op='view', tid=tid)


class TeamAddUserAPI(Resource):
    @hack_alert(permission_check)
    @login_required
    def get(self, tid, uid):
        TeamService(db).add_user(tid, uid)
        return TeamAPI().get(op='view', tid=tid)

    @hack_alert(permission_check)
    @login_required
    def post(self, tid, uid):
        uids = [int(i) for i in request.form.get('uids').split(' ')]
        for uid in uids:
            TeamService(db).add_user(tid=tid, uid=uid)
        return current_app.make_response(
            redirect(url_for('Team.team', op='view', tid=tid))
        )


class TeamDelUserAPI(Resource):

    @login_required
    def get(self, tid, uid):
        TeamService(db).del_user(tid, uid)
        return TeamAPI().get(op='view', tid=tid)


team_api.add_resource(
    TeamsAPI,
    '/teams',
    endpoint='teams'
)

team_api.add_resource(
    NewTeamAPI,
    '/Teams/new',
    endpoint='new'
)

team_api.add_resource(
    MyTeamsAPI,
    '/Teams/mine',
    endpoint='mine'
)

team_api.add_resource(
    TeamAPI,
    '/Teams/<string:op>/<int:tid>/',
    endpoint='team'
)

team_api.add_resource(
    TeamAddUserAPI,
    '/Teams/<int:tid>/add/<int:uid>',
    endpoint='add_user'
)

team_api.add_resource(
    TeamDelUserAPI,
    '/Teams/<int:tid>/del/<int:uid>',
    endpoint='del_user'
)
