# -*- coding: utf-8 -*-
from flask import Blueprint, g, redirect, render_template, current_app, request, url_for
from flask_login import login_required
from flask_restful import Api, Resource

from my_app.foundation import csrf, db
from my_app.service import UserService
from my_app.common.constant import UserRole
from my_app.models import User


user_bp = Blueprint('User', __name__)
csrf.exempt(user_bp)
user_api = Api(user_bp)


class UsersAPI(Resource):

    @login_required
    def get(self):
        user = UserService(db).get(g.user_id)
        if user.role != UserRole.ADMIN:
            return None, 404
        return current_app.make_response(render_template(
            'users.html',
            users=UserService(db).get_all(),
            user_role=UserRole
        ))


class UserAPI(Resource):

    @login_required
    def get(self, uid, op):
        me = UserService(db).get(g.user_id)
        user = UserService(db).get(uid)
        if me.role != UserRole.ADMIN and uid != g.user_id:
            return "you cannot op other user since you're not an admin", 403
        if uid == 1 and op in ['delete', 'freeze']:
            return "fuck yourself and stay away from root", 403
        if me.role == UserRole.ADMIN and op in ['delete', 'freeze', 'unfreeze']:
            if op == 'delete':
                user.delete = True
            elif op == 'freeze':
                user.pending = True
            elif op == 'unfreeze':
                user.pending = False
            db.session.commit()
            return current_app.make_response(render_template(
                'users.html',
                users=UserService(db).get_all(),
                user_role=UserRole
            ))
        if op == 'edit':
            return current_app.make_response(render_template(
                'user.html',
                user=user,
                user_role=UserRole,
                edit=True
            ))
        elif op == 'reset_pwd':
            UserService(db).rest_password(user)
        return current_app.make_response(render_template(
            'user.html',
            user=user,
            user_role=UserRole,
        ))




    @login_required
    def post(self, uid, op):
        me = UserService(db).get(g.user_id)
        if me.role != UserRole.ADMIN and uid != g.user_id:
            return None, 404
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        if me.role != UserRole.ADMIN :
            role = UserRole.NORMAL
        if uid == 1:
            role = UserRole.ADMIN  # root must be role
        user = UserService(db).get(uid)
        user.username = username
        user.email = email
        user.role = role
        db.session.commit()
        return current_app.make_response(render_template(
            'user.html',
            user=user,
            user_role=UserRole,
        ))


user_api.add_resource(
    UsersAPI,
    '/Users',
    endpoint='users'
)

user_api.add_resource(
    UserAPI,
    '/Users/<string:op>/<int:uid>/',
    endpoint='user'
)

