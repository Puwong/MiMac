from .base_alg import BaseAlg
from classification_alg import BiClassAlg, MulClassAlg, BiClassAlgCatDog
from my_app.common.constant import BaseAlgorithm


def select_alg(image):
    alg_dict = {
        BaseAlgorithm.Base: BaseAlg,
        BaseAlgorithm.BiClass: BiClassAlg,
        BaseAlgorithm.BiClassCatDog: BiClassAlgCatDog,
        BaseAlgorithm.MulClass: MulClassAlg,
    }
    return alg_dict[image.alg.alg]
