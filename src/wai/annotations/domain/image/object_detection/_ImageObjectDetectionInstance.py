from typing import Type

from wai.common.adams.imaging.locateobjects import LocatedObjects

from .._ImageInstance import ImageInstance
from .util import render_annotations_onto_image


class ImageObjectDetectionInstance(ImageInstance[LocatedObjects]):
    """
    Adds the _repr_png_ method dynamically to object-detection instances.
    """
    @classmethod
    def annotations_type(cls) -> Type[LocatedObjects]:
        return LocatedObjects

    def __getattribute__(self, item):
        if item == '_repr_png_' and self.file_info.data is not None:
            return lambda: render_annotations_onto_image(self._file_info.data, self._annotations)

        return super().__getattribute__(item)
