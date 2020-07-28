from typing import Type

from ....core.specifier import DomainSpecifier
from .._ImageInfo import ImageInfo
from ._ImageClassificationInstance import ImageClassificationInstance


class ImageClassificationDomainSpecifier(DomainSpecifier[ImageInfo, str]):
    """
    Domain specifier for images annotated with a string
    classifying the contents of the image
    """
    @classmethod
    def domain_name(cls) -> str:
        return "Image Classification Domain"

    @classmethod
    def instance_class(cls) -> Type[ImageClassificationInstance]:
        return ImageClassificationInstance
