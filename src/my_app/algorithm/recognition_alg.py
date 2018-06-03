import ujson as json
from .base_alg import BaseAlg
from my_app.common.constant import BaseAlgorithm


class RecognitionAlg(BaseAlg):

    def __init__(self, img):
        super(RecognitionAlg, self).__init__(img)
        alg = img.alg
        alg_config = json.loads(alg.config)
        self.alg = BaseAlgorithm.Recognition
        self.labels = alg_config['labels'] if alg_config and alg else ['type1']
        self.train_data_dir = ''

    def create(self, save=True):
        from my_app.common.tools import get_label_path, json2file
        info = {
            'alg': BaseAlgorithm.Recognition,
            'data': {}
        }
        json2file(info, get_label_path(g.user_id, self.image.id))

    def edit(self, label):
        pass

    def train(self):
        pass

    def predict(self):
        pass

