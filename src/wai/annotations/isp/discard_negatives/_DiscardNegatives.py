from typing import Iterable

from ...core.component import InlineStreamProcessor
from ...core.instance import Instance


class DiscardNegatives(InlineStreamProcessor[Instance]):
    """
    ISP which removes negatives from the stream.
    """
    def _process_element(self, element: Instance) -> Iterable[Instance]:
        if not element.is_negative:
            yield element
