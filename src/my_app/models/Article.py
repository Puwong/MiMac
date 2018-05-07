# -*- coding: utf-8 -*-

from my_app.foundation import db


class Article(db.Model):
    # 设计成可以分段加载的，suf_id是下一段文章的id
    # 题目限制 60 个汉字，120 个字符
    # 一段文章的限制为 10000 个汉字
    id = db.Column(db.Integer, primary_key=True)
    suf_id = db.Column(db.Integer, default=None)
    title = db.Column(db.String(128))
    context = db.Column(db.String(20480))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

