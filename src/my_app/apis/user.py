# -*- coding: utf-8 -*-
from flask import Blueprint, g, redirect, render_template, current_app
from flask_login import login_required
from flask_restful import Api, Resource

from my_app.foundation import csrf


user_bp = Blueprint('User', __name__)
csrf.exempt(user_bp)
user_api = Api(user_bp)


class UsersAPI(Resource):

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


class UserAPI(Resource):

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


user_api.add_resource(
    UsersAPI,
    '/Users',
    endpoint='users'
)

user_api.add_resource(
    UserAPI,
    '/Users/<int:uid>',
    endpoint='user'
)

