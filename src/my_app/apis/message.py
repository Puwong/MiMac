# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, g, render_template
from flask_restful import Api, Resource
from flask_login import login_required

from my_app.foundation import csrf, db
from my_app.service import MessageService, MessageBatchServiice


message_bp = Blueprint('Message', __name__)
csrf.exempt(message_bp)
message_api = Api(message_bp)


class BatchesAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'message_batches.html',
            batches=MessageBatchServiice(db).get_all(),
        ))


class BatchAPI(Resource):

    @login_required
    def get(self, bid):
        return current_app.make_response(render_template(
            'message_batch.html',
            messages=MessageService(db).get_all(batch_id=bid, sort=[('created_at', True)]),
        ))


message_api.add_resource(
    BatchesAPI,
    '/message/batches',
    endpoint='batches'
)

message_api.add_resource(
    BatchAPI,
    '/message/batch/<int:bid>',
    endpoint='batch'
)

