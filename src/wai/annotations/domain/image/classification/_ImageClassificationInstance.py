from typing import Type

from ...classification import Classification
from .._ImageInstance import ImageInstance


class ImageClassificationInstance(ImageInstance[Classification]):
    """
    An item in an image-classification data-set.
    """
    @classmethod
    def annotations_type(cls) -> Type[Classification]:
        return Classification
