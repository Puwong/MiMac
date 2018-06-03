# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api, Resource
from flask_login import login_required

from my_app.foundation import csrf


article_bp = Blueprint('Article', __name__)
csrf.exempt(article_bp)
article_api = Api(article_bp)


class ArticlesAPI(Resource):

    @login_required
    def get(self, tid):
        from my_app.tasks import test_delay_1, test_delay_2
        if tid == 1:
            test_delay_1.delay()
        else:
            test_delay_2.delay()
        return tid


article_api.add_resource(
    ArticlesAPI,
    '/articles/<int:tid>',
    endpoint='articles'
)

