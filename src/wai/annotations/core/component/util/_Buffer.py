from typing import TypeVar, List

from wai.annotations.core.stream import ThenFunction, DoneFunction

from ...stream.util import ProcessState
from .._ProcessorComponent import ProcessorComponent

ElementType = TypeVar("ElementType")


class Buffer(ProcessorComponent[ElementType, List[ElementType]]):
    """
    Utility component which buffers the entire stream into a list,
    and then just forwards the list.
    """
    # The buffered elements
    _buffer: List[ElementType] = ProcessState(lambda self: [])

    def process_element(self, element: ElementType, then: ThenFunction[List[ElementType]], done: DoneFunction):
        self._buffer.append(element)

    def finish(self, then: ThenFunction[List[ElementType]], done: DoneFunction):
        then(self._buffer)
        done()
