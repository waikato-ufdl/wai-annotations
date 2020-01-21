from abc import abstractmethod
from typing import Iterable

from wai.common.adams.imaging.locateobjects import LocatedObject

from .._InlineStreamProcessor import InlineStreamProcessor
from .._typing import InternalFormat


class Coercion(InlineStreamProcessor[InternalFormat]):
    """
    Base class for all coercions.
    """
    def _process_element(self, element: InternalFormat) -> Iterable[InternalFormat]:
        # Get the located objects from the instance
        image_info, located_objects = element

        # Process each located object
        for located_object in located_objects:
            self._process_located_object(located_object)

        return element,

    @abstractmethod
    def _process_located_object(self, located_object: LocatedObject):
        """
        Handles the processing of individual located objects.

        :param located_object:  The located object to coerce.
        """
        pass
