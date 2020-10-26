from typing import Tuple

from ...stream import ThenFunction, DoneFunction
from ...stream.util import RequiresNoFinalisation, ProcessState
from .._ProcessorComponent import ProcessorComponent, InputElementType


class Enumerator(
    RequiresNoFinalisation,
    ProcessorComponent[InputElementType, Tuple[int, InputElementType]]
):
    """
    Enumerates the elements passing through it.
    """
    _next_index: int = ProcessState(lambda self: 0)

    def process_element(
            self,
            element: InputElementType,
            then: ThenFunction[Tuple[int, InputElementType]],
            done: DoneFunction
    ):
        then((self._next_index, element))
        self._next_index += 1
