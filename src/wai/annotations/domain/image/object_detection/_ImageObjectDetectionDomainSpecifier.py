from typing import Type

from wai.common.adams.imaging.locateobjects import LocatedObjects

from ....core.domain import DomainSpecifier
from .._Image import Image
from ._ImageObjectDetectionInstance import ImageObjectDetectionInstance


class ImageObjectDetectionDomainSpecifier(DomainSpecifier[Image, LocatedObjects]):
    """
    Domain specifier for images annotated with objects
    detected within those images.
    """
    @classmethod
    def name(cls) -> str:
        return "Image Object-Detection Domain"

    @classmethod
    def description(cls) -> str:
        return "Objects detected in images, bound by a geometric shape"

    @classmethod
    def data_type(cls) -> Type[Image]:
        return Image

    @classmethod
    def annotations_type(cls) -> Type[LocatedObjects]:
        return LocatedObjects

    @classmethod
    def instance_type(cls) -> Type[ImageObjectDetectionInstance]:
        return ImageObjectDetectionInstance
