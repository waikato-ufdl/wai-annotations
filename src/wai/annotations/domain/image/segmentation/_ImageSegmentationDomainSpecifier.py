from typing import Type, Optional

from ....core.specifier import DomainSpecifier
from .._ImageInfo import ImageInfo
from ._ImageSegmentationInstance import ImageSegmentationInstance


class ImageSegmentationDomainSpecifier(DomainSpecifier[ImageInfo, Optional[ImageInfo]]):
    """
    Domain specifier for images annotated with a label for each
    pixel in the image.
    """
    @classmethod
    def domain_name(cls) -> str:
        return "Image Segmentation Domain"

    @classmethod
    def instance_class(cls) -> Type[ImageSegmentationInstance]:
        return ImageSegmentationInstance
