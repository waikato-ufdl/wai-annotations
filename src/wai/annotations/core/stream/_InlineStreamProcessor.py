from abc import abstractmethod
from functools import wraps
from typing import Generic, TypeVar, Iterator, Callable, Iterable, Any

from ..utils import chain_map

StreamElementType = TypeVar("StreamElementType")


class InlineStreamProcessor(Generic[StreamElementType]):
    """
    Base class for objects which can process a stream of elements
    in some manner. Can modify stream elements, remove or insert new
    elements, etc.

    TODO: Add batch-processing functionality to simplify stack-traces when
          debugging.
    """
    def as_decorator(self, function: Callable[[Any], Iterable[StreamElementType]]):
        """
        Allows the processor to be used as a decorator for
        functions which return an iterable, automatically processing
        the return value.

        :param function:    The function being decorated.
        :return:            The decorated function wrapper.
        """
        @wraps(function)
        def wrapper(*args, **kwargs):
            return self.process(function(*args, **kwargs))
        
        return wrapper

    def process(self, stream: Iterable[StreamElementType]) -> Iterator[StreamElementType]:
        """
        Processes the stream.

        :param stream:  The stream to process.
        :return:        The stream with processing.
        """
        return chain_map(self._process_element, stream)

    @abstractmethod
    def _process_element(self, element: StreamElementType) -> Iterable[StreamElementType]:
        """
        Processes a single element in the stream.

        :param element:     The element to process.
        :return:            The processed element.
        """
        pass
