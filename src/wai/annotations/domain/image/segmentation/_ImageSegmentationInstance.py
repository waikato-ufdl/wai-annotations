from ....core.instance import Instance
from .._ImageInfo import ImageInfo
from ._ImageSegmentationAnnotation import ImageSegmentationAnnotation


class ImageSegmentationInstance(Instance[ImageInfo, ImageSegmentationAnnotation]):
    """
    An item in an image-segmentation data-set.
    """
    @property
    def is_negative(self) -> bool:
        return self.annotations.is_negative
