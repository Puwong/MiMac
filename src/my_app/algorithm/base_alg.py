from flask import g
from my_app.common.constant import BaseAlgorithm


class BaseAlg(object):

    def __init__(self, image):
        from my_app import app_conf
        self.alg_dir = app_conf('ALG_DIR')
        self.image = image

    def create(self):
        from my_app.common.tools import get_label_path, json2file
        info = {
            'alg': BaseAlgorithm.Base,
            'data': {}
        }
        json2file(info, get_label_path(g.user_id, self.image.id))

    def edit(self, label):
        pass

    def train(self):
        pass

    def predict(self):
        pass