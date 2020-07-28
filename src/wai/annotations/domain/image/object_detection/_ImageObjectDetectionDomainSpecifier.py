from typing import Type

from wai.common.adams.imaging.locateobjects import LocatedObjects

from ....core.specifier import DomainSpecifier
from .._ImageInfo import ImageInfo
from ._ObjectDetectionInstance import ObjectDetectionInstance


class ImageObjectDetectionDomainSpecifier(DomainSpecifier[ImageInfo, LocatedObjects]):
    """
    Domain specifier for images annotated with objects
    detected within those images.
    """
    @classmethod
    def domain_name(cls) -> str:
        return "Image Object-Detection Domain"

    @classmethod
    def instance_class(cls) -> Type[ObjectDetectionInstance]:
        return ObjectDetectionInstance
