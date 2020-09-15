import numpy as np
from typing import Tuple, Optional

from wai.common import TwoWayDict


class ImageSegmentationAnnotation:
    """
    Represents the annotations for a single image in an image-segmentation
    data-set. Consists of an array of indices into a table of labels.
    """
    def __init__(self, labels: TwoWayDict[int, str], size: Tuple[int, int]):
        self._labels = labels
        self._indices: np.ndarray = np.zeros(size, np.uint16)

        self._is_negative: bool = True
        self._requires_negative_check: bool = False

    @property
    def is_negative(self):
        if self._requires_negative_check:
            self._is_negative = np.sum(self._indices) == 0
            self._requires_negative_check = False

        return self._is_negative
