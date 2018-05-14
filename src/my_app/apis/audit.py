# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api, Resource
from flask_login import login_required

from my_app.foundation import csrf


audit_bp = Blueprint('Audit', __name__)
csrf.exempt(audit_bp)
audit_api = Api(audit_bp)


class AuditsAPI(Resource):

    @login_required
    def get(self, tid):
        from my_app.tasks import test_delay_1, test_delay_2
        if tid == 1:
            test_delay_1.delay()
        else:
            test_delay_2.delay()
        return tid


audit_api.add_resource(
    AuditsAPI,
    '/audits/<int:tid>',
    endpoint='audits'
)

