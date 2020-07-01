from typing import Iterable

from ...core.component import InlineStreamProcessor
from ...core.instance import Instance


class PassThrough(InlineStreamProcessor[Instance]):
    """
    Inline stream-processor which does nothing to the stream.
    """
    def _process_element(self, element: Instance) -> Iterable[Instance]:
        return element,
