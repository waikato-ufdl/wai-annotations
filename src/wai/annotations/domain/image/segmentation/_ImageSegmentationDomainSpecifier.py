from typing import Type

from ....core.domain import DomainSpecifier
from .._Image import Image
from ._ImageSegmentationAnnotation import ImageSegmentationAnnotation
from ._ImageSegmentationInstance import ImageSegmentationInstance

DESCRIPTION = """Images segmented by category.

The image segmentation domain 'colourises' an image by assigning a category to each pixel (where no category
corresponds to 'the background'). Instances in this domain are a still image and a corresponding table of the same
size, where each element is a label.
"""


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
        return DESCRIPTION

    @classmethod
    def data_type(cls) -> Type[Image]:
        return Image

    @classmethod
    def annotations_type(cls) -> Type[ImageSegmentationAnnotation]:
        return ImageSegmentationAnnotation

    @classmethod
    def instance_type(cls) -> Type[ImageSegmentationInstance]:
        return ImageSegmentationInstance
