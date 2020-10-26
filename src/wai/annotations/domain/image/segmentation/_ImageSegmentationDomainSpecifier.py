from typing import Type

from ....core.domain import DomainSpecifier
from .._Image import Image
from ._ImageSegmentationAnnotation import ImageSegmentationAnnotation
from ._ImageSegmentationInstance import ImageSegmentationInstance


class ImageSegmentationDomainSpecifier(DomainSpecifier[Image, ImageSegmentationAnnotation]):
    """
    Domain specifier for images annotated with a label for each
    pixel in the image.
    """
    @classmethod
    def name(cls) -> str:
        return "Image Segmentation Domain"

    @classmethod
    def description(cls) -> str:
        return "Images where a class label is assigne to each pixel"

    @classmethod
    def data_type(cls) -> Type[Image]:
        return Image

    @classmethod
    def annotations_type(cls) -> Type[ImageSegmentationAnnotation]:
        return ImageSegmentationAnnotation

    @classmethod
    def instance_type(cls) -> Type[ImageSegmentationInstance]:
        return ImageSegmentationInstance
