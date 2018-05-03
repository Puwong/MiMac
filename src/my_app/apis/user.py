# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api, Resource

from my_app.foundation import csrf


user_bp = Blueprint('User', __name__)
csrf.exempt(user_bp)
user_api = Api(user_bp)


class UsersAPI(Resource):

    def get(self, tid):
        from my_app.tasks import test_delay_1, test_delay_2
        if tid == 1:
            test_delay_1.delay()
        else:
            test_delay_2.delay()
        return tid


user_api.add_resource(
    UsersAPI,
    '/Users/<int:tid>',
    endpoint='users'
)

