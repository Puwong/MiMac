# -*- coding: utf-8 -*-
import os
from flask import Blueprint, request, current_app, redirect, flash, session, render_template, url_for, g, Response
from flask_login import login_user, logout_user
from flask_restful import Api, Resource, reqparse
from .base import query_parser

from my_app.foundation import csrf, db
from my_app.service import UserService
from my_app.common.db_helper import exists_query
from my_app.models import User


auth_bp = Blueprint('Auth', __name__)
csrf.exempt(auth_bp)
auth_api = Api(auth_bp)


login_parser = query_parser.copy()
login_parser.add_argument('next', type=unicode, required=False, location='args')  # NOQA


class LoginAPI(Resource):
    def __init__(self):
        self.args = login_parser.parse_args()

    def get(self):
        user = UserService(db).get(g.user_id)
        if user and user.is_authenticated():
            resp = current_app.make_response(
                redirect(url_for('Image.images'))
            )
            return resp
        elif 'uid' in session and 'uname' in session:
            session.pop('uid')
            session.pop('uname')
        resp = current_app.make_response(render_template(
            'login.html',
        ))
        return resp

    def post(self):
        username = request.form.get('username', None)
        raw_pwd = request.form.get('password', None)
        remember = request.form.get('remember', None)
        next_url = self.args.next
        user, message = UserService(db).check_user_passwd(username, raw_pwd)
        if user is None:
            return redirect(url_for('Auth.login'))
        login_user(user, remember=remember)
        resp = current_app.make_response(
            redirect(next_url if next_url else url_for('Image.images'))
        )
        return resp


class LogoutAPI(Resource):
    def get(self):
        logout_user()
        resp = current_app.make_response(
            redirect(url_for('.login'))
        )
        return resp


register_parser = query_parser.copy()
register_parser.add_argument('username', type=unicode, required=True, location='form')  # NOQA
register_parser.add_argument('password', type=unicode, required=True, location='form')  # NOQA
register_parser.add_argument('email', type=unicode, required=True, location='form')  # NOQA


class RegisterAPI(Resource):
    def get(self):
        return Response(render_template(
            'register.html',
            can_register=True
        ))

    def post(self):
        args = register_parser.parse_args()
        username = args.get('username')
        password = UserService.generate_pwd(args.get('password'))
        email = args.get('email')
        if exists_query(User.query.filter_by(username=username)):
            return "ERROR_DUPLICATE_USER_NAME"
        user = User(
            username=username,
            password=password,
            email=email,
            pending=0,
        )
        db.session.add(user)
        db.session.commit()
        new_user = UserService(db).get_user_by_name(username)
        UserService(db).add_user_dir(new_user.id)
        login_user(new_user, remember=False)
        return redirect(url_for('Auth.login'))


auth_api.add_resource(
    LoginAPI,
    '/auth/login',
    endpoint='login'
)
auth_api.add_resource(
    LogoutAPI,
    '/auth/logout',
    endpoint='logout'
)
auth_api.add_resource(
    RegisterAPI,
    '/auth/register',
    endpoint='register'
)


frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def web_index():
    return redirect(url_for('frontend.landing'))


@frontend.route('/landing')
def landing():
    if g.user_id:
        return redirect(url_for('Image.images'))
    return render_template('base.html')