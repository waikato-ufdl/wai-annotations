from ....core.instance import Instance
from .._ImageInfo import ImageInfo


class ImageClassificationInstance(Instance[ImageInfo, str]):
    """
    An item in an image-classification data-set.
    """
    @property
    def is_negative(self) -> bool:
        return len(self.annotations) == 0
