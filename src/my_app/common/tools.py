import json
import os
from PIL import Image
from flask import g
from my_app import app_conf
from my_app.service import AlgService
from my_app.foundation import db


def resize_img(from_dir, to_dir, new_size=(224,224)):
    img = Image.open(from_dir)
    img = img.resize(new_size)
    print to_dir
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
    from my_app import app_conf
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app_conf('ALLOWED_EXTENSIONS')


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
    return get_file_path(*args, extension='label')


def get_user_file_path(filename, user_id=None):
    if user_id is None:
        user_id = g.user_id
    return get_file_path(user_id, filename)


def get_file_path(*args, **kargs):
    path = os.path.join(app_conf('USER_DIR'), *[str(i) for i in args])
    if 'extension' in kargs.keys():
        path = path + '.' + kargs['extension']
    return path


def get_alg_path(id_or_ins):
    return os.path.join(app_conf('ALG_DIR'), str(AlgService(db).get(id_or_ins).id))


def get_tiny_path(img_id):
    return get_file_path(g.user_id, str(img_id)+'.tiny.jpg')

