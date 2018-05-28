# -*- coding: utf-8 -*-
import os
import time
from flask import Flask, g, request
from flask.ext.login import current_user
from my_app.models import User
from my_app.foundation import make_celery, logger, cors, csrf, db, login_manager
from my_app import apis

DEFAULT_APP_NAME = 'MiMac'

def create_app():
    app = Flask(DEFAULT_APP_NAME)
    app.config.from_object('settings.base')
    if os.path.exists('/Users/megvii/MiMac/src/settings/local.py'):
        app.config.from_pyfile('/Users/megvii/MiMac/src/settings/local.py')
        print("load local conf successd")
    configure_foundations(app)
    configure_blueprint(app, apis.MODULES)
    # configure_handlers(app)
    configure_csrf(app)
    # configure_oauth(oauth)
    return app


def configure_csrf(app):
    cors.init_app(app, resources=app.config.get('CORS_RESOURCES', {}))
    csrf.init_app(app)


def configure_foundations(app):
    db.app = app
    db.init_app(app)
    logger.init_app(app)

    # pub_jwk.init_app(app)
    # pri_jwk.init_app(app)

    @app.after_request
    def releaseDB(response):
        from flask.ext.sqlalchemy import get_debug_queries
        total_db_duration = 0
        total_db_count = 0
        for query in get_debug_queries():
            total_db_duration += query.duration
            total_db_count += 1
        response.headers['X-DB-QUERY-DURATION'] = '%.3f' % total_db_duration
        response.headers['X-DB-QUERY-COUNT'] = total_db_count
        return response

    @app.teardown_appcontext
    def release_sessions(*args, **kwargs):
        db.session.close()

    login_manager.init_app(app)
    login_manager.login_view = 'Auth.login'
    login_manager.login_message = u'请登录'

    @login_manager.user_loader
    def load_user(id):
        try:
            return User.query.get(id)
        except Exception:
            return None

    """
    def load_by_access_token(request):
        from app.models import Token

        access_token = request.args.get('access_token', None)
        if access_token:
            token = Token.query.filter_by(access_token=access_token).first()
            if token:
                user = User.query.get(token.user_id)
                return user
        return None

    def load_by_jwt_token(request):
        from app.foundation import pri_jwk

        prefix = 'JWT '
        authorization = request.headers.get('Authorization')
        if authorization and authorization.startswith(prefix):
            token = authorization[len(prefix):]
            jwt = jose.decrypt(jose.deserialize_compact(token), pri_jwk)
            user_id = jwt.claims.get('uid', None)
            expires = jwt.claims.get('expires', 1)
            if user_id and expires > time.time():
                user = User.query.get(user_id)
                return user
        return None
    """
    def load_by_username_and_password(request):
        if app.debug:
            username = request.args.get('username')
            password = request.args.get('password')
            if username and password:
                user = User.query.filter(User.username == username).first()
                if user and user.check_password(password):
                    return user

        return None
    """
    @login_manager.request_loader
    def load_user_from_request(request):
        for func in [load_by_jwt_token, load_by_access_token,
                     load_by_username_and_password]:
            user = func(request)
            if user:
                return user
        return None
    """
    @app.before_request
    def before_request():
        from my_app.common.constant import BaseAlgorithm, ImageState
        g.user_id = current_user.id if hasattr(current_user, 'id') else None
        g.image_alg = BaseAlgorithm.AlgDict
        g.image_state = ImageState.StateDict
        now = int(time.time())
        g.TIMESTAMP = now

        # maintain = int(Config.get_config('maintain'))
        # if maintain:
        #    abort(500)

    @app.after_request
    def after_request(response):
        response.headers['X-ENDPOINT'] = request.endpoint
        return response


def configure_blueprint(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)


def app_conf(conf):
    return app.config[conf]


app = create_app()
celery = make_celery(app)


