# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api, Resource
from flask_login import login_required

from my_app.foundation import csrf


message_bp = Blueprint('Message', __name__)
csrf.exempt(message_bp)
message_api = Api(message_bp)


class MessagesAPI(Resource):

    @login_required
    def get(self, tid):
        from my_app.tasks import test_delay_1, test_delay_2
        if tid == 1:
            test_delay_1.delay()
        else:
            test_delay_2.delay()
        return tid


message_api.add_resource(
    MessagesAPI,
    '/messages/<int:tid>',
    endpoint='messages'
)

