import ujson as json
from flask import g
from .base_alg import BaseAlg
from my_app.foundation import db
from my_app.common.constant import BaseAlgorithm, ImageState


class CaptionAlg(BaseAlg):

    def __init__(self, img):
        super(CaptionAlg, self).__init__(img)
        self.alg = BaseAlgorithm.Caption
        self.train_data_dir = ''

    def create(self, save=True):
        from my_app.common.tools import get_label_path, json2file
        info = {
            'alg': BaseAlgorithm.Caption,
            'data': {
                'value': '...'
            }
        }
        json2file(info, get_label_path(g.user_id, self.image.id))

    def edit(self, value):
        from my_app.common.tools import file2json, json2file
        label = file2json(self.image.uri + '.label')
        label['data']['value'] = value
        json2file(label, self.image.uri + '.label')
        self.image.state = ImageState.DONE_LABEL
        db.session.commit()

    def train(self):
        pass

    def predict(self):
        pass

