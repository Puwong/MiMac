# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api, Resource
from flask_login import login_required

from my_app.foundation import csrf


team_bp = Blueprint('Team', __name__)
csrf.exempt(team_bp)
team_api = Api(team_bp)


class TeamsAPI(Resource):

    @login_required
    def get(self, tid):
        from my_app.tasks import test_delay_1, test_delay_2
        if tid == 1:
            test_delay_1.delay()
        else:
            test_delay_2.delay()
        return tid


team_api.add_resource(
    TeamsAPI,
    '/teams/<int:tid>',
    endpoint='teams'
)

