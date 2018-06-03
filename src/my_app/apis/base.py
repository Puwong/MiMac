import os
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse
from flask_login import login_required

from my_app.foundation import csrf

query_parser = reqparse.RequestParser()
query_parser.add_argument('page', type=int, default=1, location='args')
query_parser.add_argument('per_page', type=int, default=10, location='args')
query_parser.add_argument('sorts', type=str, location='args')
query_parser.add_argument('fields', type=str, location='args')
query_parser.add_argument('search', type=unicode, location='args')
query_parser.add_argument('all', type=unicode, location='args')

test_bp = Blueprint('Test', __name__)
csrf.exempt(test_bp)
test_api = Api(test_bp)


class TestAPI(Resource):

    @login_required
    def get(self):
        return "success"


test_api.add_resource(
    TestAPI,
    '/test',
    endpoint='test'
)

static_bp = Blueprint('Static', __name__)
csrf.exempt(static_bp)
static_api = Api(static_bp)


class StaticFilesAPI(Resource):

    def get(self, filename):
        from flask import current_app, send_from_directory
        if filename.endswith('.html'):
            abort(404)
        return send_from_directory(
            os.path.join(current_app.root_path, 'apis/static'),
            filename
        )


static_api.add_resource(
    StaticFilesAPI,
    '/my_static/<path:filename>',
    endpoint='static'
)







