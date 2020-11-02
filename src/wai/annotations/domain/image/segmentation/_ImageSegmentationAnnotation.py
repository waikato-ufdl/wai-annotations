import numpy as np
from typing import Tuple, List


class ImageSegmentationAnnotation:
    """
    Represents the annotations for a single image in an image-segmentation
    data-set. Consists of an array of indices into a table of labels.
    """
    def __init__(self, labels: List[str], size: Tuple[int, int]):
        self._labels = list(labels)
        self._size = size
        self._indices: np.ndarray = np.zeros((size[1], size[0]), np.uint16)
        self._indices.flags.writeable = False

        self._is_negative: bool = True
        self._requires_negative_check: bool = False

    @property
    def labels(self) -> List[str]:
        return list(self._labels)

    @labels.setter
    def labels(self, value: List[str]):
        if len(value) < self.max_index:
            raise Exception("Not enough labels provided for current state of indices")

        self._labels = list(value)

    @property
    def size(self) -> Tuple[int, int]:
        return self._size

    @property
    def num_labels(self) -> int:
        return len(self._labels)

    @property
    def indices(self) -> np.ndarray:
        return self._indices

    @indices.setter
    def indices(self, value: np.ndarray):
        # Make sure the array is of the correct shape/type
        if value.shape != self._indices.shape:
            raise Exception("Can't change shape of index array")
        elif value.dtype != np.uint16:
            raise Exception("Can't change type of index array")

        # Make sure there are enough labels for the indices
        if np.max(value) > len(self._labels):
            raise Exception("Not enough labels for this array")

        self._indices = value
        self._indices.flags.writeable = False

    @property
    def max_index(self) -> int:
        return np.max(self._indices)

    @property
    def is_negative(self):
        if self._requires_negative_check:
            self._is_negative = np.sum(self._indices) == 0
            self._requires_negative_check = False

        return self._is_negative
