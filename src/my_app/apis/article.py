# -*- coding: utf-8 -*-
from flask import Blueprint, g, render_template, current_app, request, redirect, url_for
from flask_login import login_required
from flask_restful import Api, Resource

from my_app.foundation import csrf, db
from my_app.service import ArticleService


article_bp = Blueprint('Article', __name__)
csrf.exempt(article_bp)
article_api = Api(article_bp)


class ArticlesAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'articles.html',
            articles=ArticleService(db).get_all(),
            all=True
        ))

    @login_required
    def post(self):
        return self.get()


class MyArticlesAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'articles.html',
            articles=ArticleService(db).get_by_user(g.user_id),
        ))

    @login_required
    def post(self):
        return self.get()


class NewArticleAPI(Resource):

    @login_required
    def get(self):
        return current_app.make_response(render_template(
            'article.html',
        ))

    @login_required
    def post(self):
        title = request.form.get('title')
        tags = request.form.get('tags').split(' ')  # TODO
        text = request.form.get('text')
        article = ArticleService(db).create(title=title, text=text)
        return current_app.make_response(
            redirect(url_for('Article.article', op='view', aid=article.id))
        )


class ArticleAPI(Resource):

    @login_required
    def get(self, aid, op):
        if op == 'edit':
            article = ArticleService(db).get(aid)
            article.visitor_count += 1
            db.session.commit()
            return current_app.make_response(render_template(
                'article.html',
                edit=True,  # actually it doesn't be used
                article=ArticleService(db).get_info(aid, with_text=True),
            ))
        elif op == 'delete':
            article = ArticleService(db).get(aid)
            article.delete = True
            db.session.commit()
            return current_app.make_response(
                redirect(url_for('Article.articles'))
            )
        return current_app.make_response(render_template(
            'article.html',
            show=True,
            article=ArticleService(db).get_info(aid, with_text=True),
        ))

    @login_required
    def post(self, aid, op):
        print 000
        if op == 'edit':
            title = request.form.get('title')
            tags = request.form.get('tags').split(' ')  # TODO
            text = request.form.get('text')
            article = ArticleService(db).update(aid, title=title, text=text)
            return self.get(aid=aid, op='view')


article_api.add_resource(
    ArticlesAPI,
    '/Articles',
    endpoint='articles'
)

article_api.add_resource(
    NewArticleAPI,
    '/Articles/new',
    endpoint='new'
)

article_api.add_resource(
    MyArticlesAPI,
    '/Articles/mine',
    endpoint='mine'
)

article_api.add_resource(
    ArticleAPI,
    '/Articles/<string:op>/<int:aid>/',
    endpoint='article'
)
