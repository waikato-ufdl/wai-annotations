from typing import Iterable

from .._StreamSource import StreamSource
from .._typing import ThenFunction, DoneFunction, ElementType


class IterableStreamSource(StreamSource[ElementType]):
    """
    A class which wraps iterables as stream-sources.
    """
    def __init__(self, iterable: Iterable[ElementType]):
        self._iterable: Iterable[ElementType] = iterable

    def produce(
            self,
            then: ThenFunction[ElementType],
            done: DoneFunction
    ):
        # Produce each element from the iterable
        for element in self._iterable:
            then(element)

        # Signal that we are done
        done()
