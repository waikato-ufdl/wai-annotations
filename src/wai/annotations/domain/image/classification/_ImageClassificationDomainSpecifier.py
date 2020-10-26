from typing import Type

from ....core.domain import DomainSpecifier
from ...classification import Classification
from .._Image import Image
from ._ImageClassificationInstance import ImageClassificationInstance


class ImageClassificationDomainSpecifier(DomainSpecifier[Image, str]):
    """
    Domain specifier for images annotated with a label
    classifying the contents of the image
    """
    @classmethod
    def name(cls) -> str:
        return "Image Classification Domain"

    @classmethod
    def description(cls) -> str:
        return "Images grouped into classes, identified by a string label"

    @classmethod
    def data_type(cls) -> Type[Image]:
        return Image

    @classmethod
    def annotations_type(cls) -> Type[Classification]:
        return Classification

    @classmethod
    def instance_type(cls) -> Type[ImageClassificationInstance]:
        return ImageClassificationInstance
