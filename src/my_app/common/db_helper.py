#! encoding=utf-8
import math
from my_app.foundation import db


def count_where(*filters):
    return db.session.query(db.func.count(1)).filter(*filters).scalar()


def exists_query(q):
    return db.session.query(q.exists()).scalar()


def count_from(db_cls, *filters):
    return db.session.query(db.func.count('1'))\
             .filter(*filters)\
             .select_from(db_cls).scalar()


class MyPaginate(object):
    def __init__(self):
        self.items = []
        self.per_page = 10
        self.pages = 1
        self.page = 1


def fetch_query_paginate(db_model, query, current_page=1, page_size=10):
    fetch_page = query \
        .limit(page_size)\
        .offset((current_page - 1) * page_size)\
        .all()
    pag = MyPaginate()
    pag.items = fetch_page
    pag.per_page = page_size
    pag.pages = math.ceil(count_from(db_model) / page_size)
    pag.page = current_page
    return pag


def insert_batch_data(db_cls, rows, auto_commit=True):
    db.session.execute(db_cls.__table__.insert(), rows)
    if auto_commit:
        db.session.commit()
    else:
        db.session.flush()

