from abc import abstractmethod
from typing import Generic, TypeVar, Iterator, Callable, Iterable, Any

StreamElementType = TypeVar("StreamElementType")


class InlineStreamProcessor(Generic[StreamElementType]):
    """
    Base class for objects which can process a stream of elements
    in some manner. Can modify stream elements, remove or insert new
    elements, etc.
    """
    def as_decorator(self, function: Callable[[Any], Iterable[StreamElementType]]):
        """
        Allows the processor to be used as a decorator for
        functions which return an iterable, automatically processing
        the return value.

        :param function:    The function being decorated.
        :return:            The decorated function wrapper.
        """
        def wrapper(*args, **kwargs):
            return self.process(function(*args, **kwargs))
        
        return wrapper

    def process(self, stream: Iterable[StreamElementType]) -> Iterator[StreamElementType]:
        """
        Processes the stream.

        :param stream:  The stream to process.
        :return:        The stream with processing.
        """
        # Process each element in turn
        for element in stream:
            # Process the element
            processed = self._process_element(element)

            for processed_element in processed:
                yield processed_element

    @abstractmethod
    def _process_element(self, element: StreamElementType) -> Iterable[StreamElementType]:
        """
        Processes a single element in the stream.

        :param element:     The element to process.
        :return:            The processed element.
        """
        pass
