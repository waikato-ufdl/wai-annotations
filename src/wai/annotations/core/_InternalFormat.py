from wai.common.adams.imaging.locateobjects import LocatedObjects

from ._ImageInfo import ImageInfo


class InternalFormat:
    """
    Internal format for conversions that acts like a tuple of [ImageInfo, LocatedObjects]
    with some extra functionality.
    """
    def __init__(self, image_info: ImageInfo, located_objects: LocatedObjects):
        self._image_info: ImageInfo = image_info
        self._located_objects: LocatedObjects = located_objects

    @property
    def image_info(self) -> ImageInfo:
        return self._image_info

    @property
    def located_objects(self) -> LocatedObjects:
        return self._located_objects

    def __iter__(self):
        return iter((self.image_info, self.located_objects))