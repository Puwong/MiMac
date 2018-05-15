# -*- coding: utf-8 -*-
import os
from flask import Blueprint, abort, current_app, redirect, flash, session, render_template, url_for, g, Response
from flask_login import login_user, logout_user
from flask_restful import Api, Resource, reqparse
from .base import query_parser

from my_app.foundation import csrf, db
from my_app.forms import LoginForm
from my_app.service import UserService
from my_app.common.constant import LoginState
from my_app.common.db_helper import exists_query
from my_app.models import User


auth_bp = Blueprint('Auth', __name__)
csrf.exempt(auth_bp)
auth_api = Api(auth_bp)


login_parser = query_parser.copy()
login_parser.add_argument('next', type=unicode, required=False, location='args')  # NOQA
FRONTEND_ = "/api/files"

class LoginAPI(Resource):
    def __init__(self):
        self.form = LoginForm()
        self.args = login_parser.parse_args()

    def get(self):
        if g.user and g.user.is_authenticated():
            resp = current_app.make_response(
                redirect(FRONTEND_)
            )
            resp.set_cookie('status', LoginState.STATE_ONLINE)
            return resp
        elif 'uid' in session and 'uname' in session:
            session.pop('uid')
            session.pop('uname')
        resp = current_app.make_response(render_template(
            'login.html',
            form=self.form
        ))
        resp.set_cookie('status', LoginState.STATE_OFFLINE)
        return resp

    def post(self):
        username = self.form.username.data
        password = self.form.password.data
        remember = self.form.remember_me.data
        next_url = self.args.next
        user, message = UserService().check_user_passwd(username, password)
        if user is None:
            flash(message, 'danger')
            return redirect(url_for('Auth.auth-login'))
        login_user(user, remember=remember)
        resp = current_app.make_response(
            redirect(next_url or FRONTEND_)
        )
        #resp.set_cookie('status', LoginState.STATE_ONLINE)
        return resp


class StaticFilesAPI(Resource):
    def get(self, filename):
        from flask import current_app, send_from_directory
        if filename.endswith('.html'):
            abort(404)
        return send_from_directory(
            os.path.join(current_app.root_path, 'templates/page_'),
            filename
        )


register_page_parser = reqparse.RequestParser()
register_page_parser.add_argument('code', type=unicode, required=False, location='args') # NOQA

register_parser = query_parser.copy()
register_parser.add_argument('username', type=unicode, required=True, location='form')  # NOQA
register_parser.add_argument('password', type=unicode, required=True, location='form')  # NOQA
register_parser.add_argument('email', type=unicode, required=True, location='form')  # NOQA


class RegisterAPI(Resource):
    def get(self):
        args = register_page_parser.parse_args()
        return Response(render_template(
            'register.html',
            can_register=True
        ))

    def post(self):
        args = register_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        email = args.get('email')
        print username
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
        new_user = UserService().get_user_by_name(username)
        UserService().add_user_dir(new_user.id)
        login_user(new_user, remember=False)
        return redirect(url_for('Auth.auth-login'))


auth_api.add_resource(
    StaticFilesAPI,
    '/auth/<path:filename>',
    endpoint='auth-static-files'
)
auth_api.add_resource(
    LoginAPI,
    '/auth/login',
    endpoint='auth-login'
)
auth_api.add_resource(
    RegisterAPI,
    '/auth/register',
    endpoint='auth-register'
)

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def web_index():
    return redirect(url_for('frontend.landing'))


@frontend.route('/landing')
def landing():
    return render_template('landing.html')