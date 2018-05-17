from .base_alg import BaseAlg
from classification_alg import BiClassAlg, MulClassAlg, BiClassAlgCatDog
from my_app.common.constant import ImageAlgorithm


def select_alg(image):
    alg_dict = {
        ImageAlgorithm.Base: BaseAlg,
        ImageAlgorithm.BiClass: BiClassAlg,
        ImageAlgorithm.BiClassCatDog: BiClassAlgCatDog,
        ImageAlgorithm.MulClass: MulClassAlg,
    }
    return alg_dict[image.alg]
