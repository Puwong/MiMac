from flask import Blueprint
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












