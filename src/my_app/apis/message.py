# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, g, render_template, request, redirect, url_for
from flask_restful import Api, Resource
from flask_login import login_required

from my_app.foundation import csrf, db
from my_app.service import MessageService, MessageBatchServiice
from my_app.common.constant import MessageType


message_bp = Blueprint('Message', __name__)
csrf.exempt(message_bp)
message_api = Api(message_bp)


class BatchesAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'message_batches.html',
            batches=MessageBatchServiice(db).get_all(filters=['by_user']),
        ))

    @login_required
    def post(self):
        return self.get()


class BatchAPI(Resource):

    @login_required
    def get(self, bid, op):
        return current_app.make_response(render_template(
            'message_batch.html',
            show=True,
            batch=MessageBatchServiice(db).get_info(bid),
        ))


class NewBatchAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'message_batch.html',
            new=True,
            message_type=MessageType
        ))

    @login_required
    def post(self):
        title = request.form.get('title')
        type = request.form.get('type')
        context = request.form.get('context')
        to_uid = request.form.get('to_uid')
        message_batch = MessageBatchServiice(db).create(title=title, to_uid=to_uid, type=type, context=context)
        return current_app.make_response(
            redirect(url_for('Message.batches'))
        )


message_api.add_resource(
    BatchesAPI,
    '/message/batches',
    endpoint='batches'
)

message_api.add_resource(
    NewBatchAPI,
    '/message/batches/new',
    endpoint='new'
)

message_api.add_resource(
    BatchAPI,
    '/message/batch/<string:op>/<int:bid>',
    endpoint='batch'
)

