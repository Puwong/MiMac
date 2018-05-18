from flask import g
from my_app.common.constant import ImageAlgorithm


class BaseAlg(object):

    def __init__(self, image):
        self.image = image

    def create(self):
        from my_app.common.tools import get_label_path, json2file
        info = {
            'alg': ImageAlgorithm.Base,
            'data': {}
        }
        json2file(info, get_label_path(g.user_id, self.image.id))

    def edit(self, label):
        pass

    def train(self):
        pass

    def predict(self):
        pass