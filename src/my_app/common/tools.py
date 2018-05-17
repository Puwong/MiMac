import json
import os
from PIL import Image
from flask import g
from my_app import app_conf


def resize_img(from_dir, to_dir, new_size=(224,224)):
    img = Image.open(from_dir)
    img = img.resize(new_size)
    img.save(to_dir)


def json2file(my_json, my_file):
    with open(my_file, 'w') as f:
        f.write(json.dumps(my_json))


def file2json(my_file):
    with open(my_file) as f:
        return json.loads((f.read()))


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


