import itertools
from typing import Iterable, TypeVar, Callable, Iterator, Optional

from ..debug import get_debug, DebugIterableCache

InputElementType = TypeVar("InputElementType")
OutputElementType = TypeVar("OutputElementType")


def chain_map(func: Callable[[InputElementType], Iterable[OutputElementType]],
              iterable: Iterable[InputElementType],
              cache: Optional[bool] = None) -> Iterator[OutputElementType]:
    """
    Applies a mapping that produces an iterator per element of
    the input iterable, and chains the mapped iterators.

    :return:    An iterator over the mapped elements.
    """
    # If no value is provided for caching, decide based on the debug setting
    if cache is None:
        cache = get_debug()

    # If caching, use recursion for processing but add the caching layer
    if cache:
        output_cache = DebugIterableCache(chain_map(func, iterable, False))
        return output_cache

    # Otherwise just chain the results of processing each element
    return itertools.chain.from_iterable(map(func, iterable))
