from typing import Iterable

from ._typing import InternalFormat
from ._InlineStreamProcessor import InlineStreamProcessor


class DuplicateImageNames(InlineStreamProcessor[InternalFormat]):
    """
    Processes a stream of images ensuring that the same
    image name doesn't appear twice.
    """
    def __init__(self):
        self._seen_names = set()

    def _process_element(self, element: InternalFormat) -> Iterable[InternalFormat]:
        # Get the image name from the element
        image_name = element[0].filename

        # If we've seen it, raise an error
        if image_name in self._seen_names:
            raise ValueError(f"Image named '{image_name}' appear multiple times during conversion")

        # Add the name to the set of seen images
        self._seen_names.add(image_name)

        return element,