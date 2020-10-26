import itertools
from typing import Iterable, TypeVar, Callable, Iterator

InputElementType = TypeVar("InputElementType")
OutputElementType = TypeVar("OutputElementType")


def chain_map(func: Callable[[InputElementType], Iterable[OutputElementType]],
              iterable: Iterable[InputElementType]) -> Iterator[OutputElementType]:
    """
    Applies a mapping that produces an iterator per element of
    the input iterable, and chains the mapped iterators.

    :return:    An iterator over the mapped elements.
    """
    return itertools.chain.from_iterable(map(func, iterable))
