from typing import Iterator, TypeVar, Iterable

ElementType = TypeVar("ElementType")


class DebugIterableCache(Iterator[ElementType]):
    """
    A cache of an iterable which is it's own iterator.
    """
    def __init__(self, source: Iterable[ElementType]):
        self._source = list(source)
        self._iter = iter(self._source)

    def __next__(self) -> ElementType:
        return next(self._iter)
