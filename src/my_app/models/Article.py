# -*- coding: utf-8 -*-
import time

from my_app.foundation import db
from .TextNode import TextNode


class Article(db.Model):
    # 设计成可以分段加载的，一次性把所有的text_node加载进来按时间排序
    # 题目限制 60 个汉字，120 个字符
    # 一段文章的限制为 10000 个汉字
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(128))
    text_nodes = db.relationship("TextNode", backref="article", lazy='dynamic')
    delete = db.Column(db.Boolean, default=False)
    visitor_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Integer, default=time.time)
    modified_at = db.Column(db.Integer, default=time.time, onupdate=time.time)

