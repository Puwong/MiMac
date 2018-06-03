# -*- coding: utf-8 -*-
from my_app.foundation import db


class AlgUserRelationship(db.Model):
    #  因为设计上有些东西没有想明白，比如如果某一个管理员删除了一个算法后
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    alg_id = db.Column(db.Integer, db.ForeignKey('alg.id'))
