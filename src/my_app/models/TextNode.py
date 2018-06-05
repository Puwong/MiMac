# -*- coding: utf-8 -*-

from my_app.foundation import db
import time


class TextNode(db.Model):
    # 一段文章的限制为 10000 个汉字
    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.String(2048))
    created_at = db.Column(db.Integer, default=time.time)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

