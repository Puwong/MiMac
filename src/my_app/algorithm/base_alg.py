import os
from flask import g
from my_app.common.constant import BaseAlgorithm


class BaseAlg(object):

    def __init__(self, image):
        from my_app.common.tools import get_alg_path
        self.alg = BaseAlgorithm.Base
        self.alg_dir = get_alg_path(image.alg)
        self.model_weight = os.path.join(self.alg_dir, 'weight.h5')
        self.model = os.path.join(self.alg_dir, 'model.json')
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

    def predict_check(self):
        return os.path.isfile(self.model) and os.path.isfile(self.model_weight)

    def predict(self):
        pass

