from my_app import celery
from my_app.common.tools import get_time_format


@celery.task
def test_delay_1():
    print("test_delay_1 called {}".format(get_time_format()))


@celery.task
def test_delay_2():
    print("test_delay_2 called {}".format(get_time_format()))


@celery.task
def predict(image_id):
    print "predict called--------------------"
    from my_app.service import ImageService
    from my_app import db
    image = ImageService(db).get(image_id)
    ImageService.algorithm(image).predict()


@celery.task
def train():
    pass


@celery.task
def test_cron_1():
    print("test_cron_1 called {}".format(get_time_format()))


@celery.task
def test_cron_2():
    print("test_cron_2 called {}".format(get_time_format()))








