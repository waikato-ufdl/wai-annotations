from typing import Type

from ....core.specifier import DomainSpecifier
from .._ImageInfo import ImageInfo


class ImageClassificationDomainSpecifier(DomainSpecifier):
    """
    Domain specifier for images annotated with a string
    classifying the contents of the image
    """
    @classmethod
    def domain_name(cls) -> str:
        return "Image Classification Domain"
    
    @classmethod
    def file_type(cls) -> Type[ImageInfo]:
        return ImageInfo

    @classmethod
    def annotations_type(cls) -> Type:
        return str
