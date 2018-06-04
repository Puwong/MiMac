# -*- coding: utf-8 -*-
import ujson as json
from flask import Blueprint, current_app, render_template, request, redirect, url_for, g
from flask_restful import Api, Resource
from flask_login import login_required

from my_app.foundation import csrf, db
from my_app.common.constant import BaseAlgorithm, UserRole
from my_app.models import Alg, AlgUserRelationship
from my_app.service import AlgService, UserService


alg_bp = Blueprint('Alg', __name__)
csrf.exempt(alg_bp)
alg_api = Api(alg_bp)


class AlgsAPI(Resource):

    @login_required
    def get(self):
        print AlgService(db).get_all()
        print AlgService(db).get_my_alg_ids()
        return current_app.make_response(render_template(
            'algs.html',
            algs=AlgService(db).get_all(),
            base_alg=BaseAlgorithm.AlgDict,
            my_algs=AlgService(db).get_my_alg_ids(),
            isAdmin=(UserService(db).get(g.user_id).role == UserRole.ADMIN)
        ))


class DelAlgAPI(Resource):

    @login_required
    def get(self, id):
        alg = AlgService(db).get(id)
        db.session.delete(alg)
        db.session.commit()
        return current_app.make_response(
            redirect(url_for('Alg.algs'))
        )


class Add2UserAPI(Resource):

    @login_required
    def post(self):
        a_ids = request.form.get('a_id').split(',')
        for a_id in a_ids:
            AlgService(db).add2user(int(a_id))
        return current_app.make_response(
            redirect(url_for('Alg.algs'))
        )


class NewAlgAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'alg.html',
            base_algs=BaseAlgorithm
        ))

    @login_required
    def post(self):
        title = request.form.get('title')
        base = request.form.get('base')
        labels = request.form.get('labels').split(' ')
        AlgService(db).create(title=title, base=base, config=json.dumps({
            'class_cnt': len(labels),
            'labels': labels
        }))
        return current_app.make_response(
            redirect(url_for('Alg.algs'))
        )


class AlgAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'algs.html',
            alg=Alg.query.all(),
            base_alg=BaseAlgorithm.AlgDict,
        ))

    @login_required
    def post(self):
        title = request.form.get('title')
        base = request.form.get('base')
        alg = Alg(title=title, base=base)
        db.session.commit()
        return current_app.make_response(
            redirect(url_for('Alg.algs'))
        )


alg_api.add_resource(
    AlgsAPI,
    '/algs',
    endpoint='algs'
)

alg_api.add_resource(
    AlgAPI,
    '/algs/<int:id>',
    endpoint='alg'
)

alg_api.add_resource(
    NewAlgAPI,
    '/algs/new',
    endpoint='new_alg'
)

alg_api.add_resource(
    DelAlgAPI,
    '/algs/del/<int:id>',
    endpoint='del_alg'
)

alg_api.add_resource(
    Add2UserAPI,
    '/algs/add2user/',
    endpoint='add2user'
)