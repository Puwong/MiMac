import json
import os
import datetime
from PIL import Image
from flask import g
from my_app.common.constant import AppConfig


def convert_file(dcm_file_path, jpg_file_path):
    import cv2
    import dicom
    import numpy as np
    dicom_img = dicom.read_file(dcm_file_path)
    img = dicom_img.pixel_array
    scaled_img = cv2.convertScaleAbs(img-np.min(img), alpha=(255.0 / min(np.max(img)-np.min(img), 10000)))
    cv2.imwrite(jpg_file_path, scaled_img)


def resize_img(from_dir, to_dir, new_size=(224,224)):
    img = Image.open(from_dir)
    img = img.resize(new_size)
    img.save(to_dir)


def json2file(my_json, file_dir):
    with open(file_dir, 'w') as f:
        f.write(json.dumps(my_json))


def file2json(file_dir):
    data = None
    if os.path.isfile(file_dir):
        with open(file_dir) as f:
            data = f.read()
    return json.loads(data) if data else None


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in AppConfig.ALLOWED_EXTENSIONS


def remove_dir_loop(my_dir):
    if os.path.isdir(my_dir):
        for p in os.listdir(my_dir):
            remove_dir_loop(os.path.join(my_dir, p))
        if os.path.exists(my_dir):
            os.rmdir(my_dir)
    else:
        if os.path.exists(my_dir):
            os.remove(my_dir)


def create_dir_loop(my_dir):
    dirs = my_dir.split('/')
    total_dir = ''
    for dir in dirs:
        total_dir += dir + '/'
        if not os.path.isdir(total_dir):
            os.mkdir(total_dir)


def get_label_path(*args):
    return get_file_path(*args, extension='jpg.label')


def get_user_file_path(filename, user_id=None):
    if user_id is None:
        user_id = g.user_id
    return get_file_path(user_id, filename, extension='jpg')


def get_file_path(*args, **kargs):
    path = os.path.join(AppConfig.USER_DIR, *[str(i) for i in args])
    if 'extension' in kargs.keys():
        path = path + '.' + kargs['extension']
    return path


def get_time_format(now=None, date_format="%Y-%m-%d %H:%M:%S"):
    if type(now) == float:  # come from time.time()
        now = datetime.datetime.fromtimestamp(now)
    elif type(now) == datetime.datetime:  # come from datetime.datetime.now()
        pass
    else:
        now = datetime.datetime.now()
    return now.strftime(date_format)

