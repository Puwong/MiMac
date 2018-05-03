import os
import math
import logging

from celery import Celery
from flask import abort
from flask.ext.cors import CORS
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect

from flask.ext.sqlalchemy import SQLAlchemy, Pagination, BaseQuery


class Logger(object):

    def __init__(self):
        pass

    def init_app(self, app):
        log_dir = './log' if app.config['DEBUG'] else app.config['LOGGER_PATH']

        self.edit_logger = self.init_logger(
            app.config['LOGGER_EDIT_SUBMIT'], log_dir)
        self.logger = self.init_logger(app.config['LOGGER_NORMAL'], log_dir)
        self.error_logger = self.init_logger(app.config['LOGGER_ERROR'], log_dir)  # NOQA E501
        self.debug_logger = self.init_logger(app.config['LOGGER_DEBUG'], log_dir)  # NOQA E501

    def init_logger(self, log_type, log_dir):
        logger = logging.getLogger(log_type)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        fh = logging.FileHandler(os.path.join(log_dir, log_type))
        formatter = logging.Formatter(
            '%(asctime)s##%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        return logger

    @staticmethod
    def _decode(s):
        if isinstance(s, str):
            return s.decode('utf-8')
        if isinstance(s, unicode):
            return s
        try:
            return '%s' % str(s)
        except UnicodeDecodeError, e:
            return 'DECODE_ERROR %s' % e

    def log(self, *pars):
        self.logger.info('|'.join([Logger._decode(s) for s in pars]))

    def error_log(self, *pars):
        self.error_logger.error('|'.join([Logger._decode(s) for s in pars]))

    def debug_log(self, *pars):
        self.debug_logger.debug('|'.join([Logger._decode(s) for s in pars]))

    def edit_submit_log(self, *pars):
        self.edit_logger.info('|'.join([Logger._decode(s) for s in pars]))



def make_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def paginate(self, page, per_page=10, error_out=False, with_entities=[]):
    if error_out and page < 1:
        abort(404)

    if with_entities:
        total = self.with_entities(*with_entities).order_by(None).count()
    else:
        total = self.order_by(None).count()
    if per_page == -1:
        page = 1
        per_page = total
    else:
        page = max(1, min(int(math.ceil(float(total) / float(per_page))), page))  # NOQA
    items = self.limit(per_page).offset((page - 1) * per_page).all()

    return Pagination(self, page, per_page, total, items)


db = SQLAlchemy(session_options={'autocommit': False, 'autoflush': False})
BaseQuery.paginate = paginate

csrf = CsrfProtect()
login_manager = LoginManager()
logger = Logger()
cors = CORS()

