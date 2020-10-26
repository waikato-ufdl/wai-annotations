from abc import abstractmethod
from typing import Generic

from ._typing import ElementType


class StreamSink(Generic[ElementType]):
    """
    A consumer of elements in a stream.
    """
    def start(self):
        """
        Performs any setup required before a stream is consumed.
        """
        pass

    @abstractmethod
    def consume_element(self, element: ElementType):
        """
        Consumes a single element from a stream.

        :param element:     The element to consume.
        """
        raise NotImplementedError(self.consume_element.__qualname__)

    @abstractmethod
    def finish(self):
        """
        Performs any finalisation once the stream is exhausted. 'consume_element'
        won't be called again after this is called.
        """
        raise NotImplementedError(self.finish.__qualname__)
