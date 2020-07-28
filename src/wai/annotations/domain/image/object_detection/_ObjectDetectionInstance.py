from wai.common.adams.imaging.locateobjects import LocatedObjects

from ....core.instance import Instance
from .._ImageInfo import ImageInfo
from .util import render_annotations_onto_image


class ObjectDetectionInstance(Instance[ImageInfo, LocatedObjects]):
    """
    Adds the _repr_png_ method dynamically to object-detection instances.
    """
    @property
    def is_negative(self) -> bool:
        return len(self.annotations) == 0

    def __getattribute__(self, item):
        if item == '_repr_png_' and self.file_info.data is not None:
            return lambda: render_annotations_onto_image(self._file_info.data, self._annotations)

        return super().__getattribute__(item)
