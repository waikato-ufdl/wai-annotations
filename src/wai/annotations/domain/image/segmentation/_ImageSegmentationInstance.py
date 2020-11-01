from typing import Type, Optional

from .._Image import Image
from .._ImageInstance import ImageInstance
from ._ImageSegmentationAnnotation import ImageSegmentationAnnotation


class ImageSegmentationInstance(ImageInstance[ImageSegmentationAnnotation]):
    """
    An item in an image-segmentation data-set.
    """
    def __init__(self, data: Image, annotations: Optional[ImageSegmentationAnnotation]):
        # Make sure the data and annotation images are the same size
        if annotations is not None and data.size != annotations.size:
            raise Exception(f"Image size {data.size} does not match segments size {annotations.size}")

        super().__init__(data, annotations)

    @classmethod
    def annotations_type(cls) -> Type[ImageSegmentationAnnotation]:
        return ImageSegmentationAnnotation
