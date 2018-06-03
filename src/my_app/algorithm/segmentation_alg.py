import ujson as json
from .base_alg import BaseAlg
from my_app.common.constant import BaseAlgorithm


class SemanticSegmentationAlg(BaseAlg):

    def __init__(self, img):
        super(SemanticSegmentationAlg, self).__init__(img)
        alg = img.alg
        alg_config = json.loads(alg.config)
        self.alg = BaseAlgorithm.SemanticSegmentation
        self.labels = alg_config['labels'] if alg_config and alg else ['type1']
        self.train_data_dir = ''

    def create(self, save=True):
        from my_app.common.tools import get_label_path, json2file
        info = {
            'alg': BaseAlgorithm.SemanticSegmentation,
            'data': {}
        }
        json2file(info, get_label_path(g.user_id, self.image.id))


class PanopticSegmentationAlg(BaseAlg):

    def __init__(self, img):
        super(PanopticSegmentationAlg, self).__init__(img)
        alg = img.alg
        alg_config = json.loads(alg.config)
        self.alg = BaseAlgorithm.PanopticSegmentation
        self.labels = alg_config['labels'] if alg_config and alg else ['type1']
        self.train_data_dir = ''

    def create(self, save=True):
        from my_app.common.tools import get_label_path, json2file
        info = {
            'alg': BaseAlgorithm.PanopticSegmentation,
            'data': {}
        }
        json2file(info, get_label_path(g.user_id, self.image.id))


class InstanceSegmentationAlg(BaseAlg):

    def __init__(self, img):
        super(InstanceSegmentationAlg, self).__init__(img)
        alg = img.alg
        alg_config = json.loads(alg.config)
        self.alg = BaseAlgorithm.InstanceSegmentation
        self.labels = alg_config['labels'] if alg_config and alg else ['type1']
        self.train_data_dir = ''

    def create(self, save=True):
        from my_app.common.tools import get_label_path, json2file
        info = {
            'alg': BaseAlgorithm.InstanceSegmentation,
            'data': {}
        }
        json2file(info, get_label_path(g.user_id, self.image.id))

