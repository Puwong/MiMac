from datetime import datetime


def now2log():
    return datetime2log(datetime.now())


def datetime2log(my_time):
    return my_time.strftime("%Y-%m-%d %H:%M:%S")
