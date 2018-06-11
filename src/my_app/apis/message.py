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
            message_type=MessageType,
            batch=MessageBatchServiice(db).get_info(bid, with_message=True, with_reply=True),
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
        type = int(request.form.get('type'))
        context = request.form.get('context')
        to_uid = int(request.form.get('to_uid'))
        message_batch = MessageBatchServiice(db).create(title=title, to_uid=to_uid, type=type, context=context)
        return current_app.make_response(
            redirect(url_for('Message.batches'))
        )


class ReplyAPI(Resource):

    @login_required
    def get(self, bid, mid, yes):
        return current_app.make_response(render_template(
            'message_batch.html',
            reply=mid,
            message_type=MessageType,
            context=MessageService(db).reply_context(mid, yes),
            batch=MessageBatchServiice(db).get_info(bid, with_message=True, with_reply=True),
        ))

    @login_required
    def post(self, bid, mid, yes):
        type = int(request.form.get('type'))
        context = request.form.get('context')
        reply_message_id = int(request.form.get('reply_message_id', 0))
        if context is None:
            return self.get(bid, reply_message_id, yes)
        message_batch = MessageBatchServiice(db).reply(bid, reply_message_id, type, context)
        return current_app.make_response(
            redirect(url_for('Message.batch', bid=bid, op='show'))
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
    ReplyAPI,
    '/message/reply/<int:bid>/<int:mid>/<int:yes>',
    endpoint='reply'
)

message_api.add_resource(
    BatchAPI,
    '/message/batch/<string:op>/<int:bid>',
    endpoint='batch'
)

