from .base_alg import BaseAlg
from .classification_alg import BiClassAlg, ClassificationAlg
from .segmentation_alg import InstanceSegmentationAlg, SemanticSegmentationAlg, PanopticSegmentationAlg
from .recognition_alg import RecognitionAlg
from .caption_alg import CaptionAlg
from my_app.common.constant import BaseAlgorithm


def select_alg(image):
    alg_dict = {
        BaseAlgorithm.BiClass: BiClassAlg,
        BaseAlgorithm.Classification: ClassificationAlg,
        BaseAlgorithm.Recognition: RecognitionAlg,
        BaseAlgorithm.InstanceSegmentation: InstanceSegmentationAlg,
        BaseAlgorithm.SemanticSegmentation: SemanticSegmentationAlg,
        BaseAlgorithm.PanopticSegmentation: PanopticSegmentationAlg,
        BaseAlgorithm.Caption: CaptionAlg
    }
    if image.alg.base in alg_dict.keys():
        return alg_dict[image.alg.base]
    else:
        return BaseAlg
