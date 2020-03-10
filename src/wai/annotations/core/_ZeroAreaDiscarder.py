from typing import Iterable

from wai.common.adams.imaging.locateobjects import LocatedObjects

from ._InlineStreamProcessor import InlineStreamProcessor
from ._typing import InternalFormat


class ZeroAreaDiscarder(InlineStreamProcessor[InternalFormat]):
    """
    Stream processor which removes annotations with zero area.
    """
    def _process_element(self, element: InternalFormat) -> Iterable[InternalFormat]:
        # Unpack the format
        image_info, located_objects = element

        # Create a new set of located objects with only non-zero-area annotations
        located_objects = LocatedObjects((located_object
                                          for located_object in located_objects
                                          if (located_object.width != 0
                                              and located_object.height != 0)
                                          or (located_object.has_polygon()
                                              and located_object.get_actual_polygon().area() != 0)))

        return (image_info, located_objects),
