from .base_alg import BaseAlg
from classification_alg import BiClassAlg, MulClassAlg
from my_app.common.constant import BaseAlgorithm


def select_alg(image):
    alg_dict = {
        BaseAlgorithm.BiClass: BiClassAlg,
        BaseAlgorithm.Classification: MulClassAlg,
    }
    if image.alg.base in alg_dict.keys():
        return alg_dict[image.alg.base]
    else:
        return BaseAlg
