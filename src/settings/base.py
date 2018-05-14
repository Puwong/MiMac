# -*- coding: utf-8 -*-

import os
from celery.schedules import crontab

PROJECT_DIR = "/Users/megvii/MiMac"

SECRET_KEY = 'mimac_default'

CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = 3600 * 48

SQLALCHEMY_POOL_RECYCLE = 10
SUPER_USER_PASSWD = 'mimac_default'

MYSQL_USER = 'mimac_default'
MYSQL_PASS = 'mimac_default'
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_DB = 'mimac'

SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)   # noqa

LOGGER_SCREEN_OPEND = False
LOGGER_PATH = os.path.join(PROJECT_DIR, 'logs')
LOGGER_EDIT_SUBMIT = "logger_edit_submit.log"
LOGGER_NORMAL = "logger_normal.log"
LOGGER_ERROR = "logger_error.log"
LOGGER_DEBUG = "logger_debug.log"

UPLOAD_FOLDER = PROJECT_DIR + '/file'
ALLOWED_EXTENSIONS = set(['dicm', 'png', 'jpg', 'jpeg', 'gif', 'log', 'json'])

TRAIN_DIR = PROJECT_DIR + 'data'

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/3')
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ['my_app.tasks']
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/4')  # NOQA
CELERY_TASK_RESULT_EXPIRES = 3 * 24 * 3600
CELERY_IGNORE_RESULT = False
# restart worker processes after every task
CELERYD_MAX_TASKS_PER_CHILD = 1000
CELERY_DISABLE_RATE_LIMITS = True
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_TRACK_STARTED = True

CELERYBEAT_SCHEDULE = {
    'timer-clean-expired-data': {
        'task': 'my_app.tasks.test_cron_1',
        'schedule': crontab(hour=2, minute=40),
    },
    'schedule-send-api-statistics': {
        'task': 'my_app.tasks.test_cron_2',
        'schedule': crontab(hour=11, minute=0, day_of_week=[1, 2, 3, 4, 5]),
    },
}

CELERY_ROUTES = {
    'my_app.tasks.test_delay_1': {'queue': 'app_logic'},
    'my_app.tasks.test_delay_2': {'queue': 'app_simple_logic'},

    'my_app.tasks.test_cron_1': {'queue': 'cron_timer'},  # NOQA: E501
    'my_app.tasks.test_cron_2': {'queue': 'cron_timer'},
}

CORS_RESOURCES = {
    r'/api/*': {
        'Access-Control-Allow-Origin': '*'
    }
}

