from my_app import celery
from my_app.common.view_helper import now2log


@celery.task
def test_delay_1():
    print("test_delay_1 called {}".format(now2log()))


@celery.task
def test_delay_2():
    print("test_delay_2 called {}".format(now2log()))

@celery.task
def predict():
    pass

@celery.task
def test_cron_1():
    print("test_cron_1 called {}".format(now2log()))


@celery.task
def test_cron_2():
    print("test_cron_2 called {}".format(now2log()))








