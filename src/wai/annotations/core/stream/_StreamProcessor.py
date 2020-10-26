from abc import abstractmethod
from typing import Generic, TypeVar

from ._typing import ThenFunction, DoneFunction

InputElementType = TypeVar("InputElementType")
OutputElementType = TypeVar("OutputElementType")


class StreamProcessor(Generic[InputElementType, OutputElementType]):
    """
    Base class for objects which can process a stream of elements
    in some manner. Can modify stream elements, remove or insert new
    elements, etc.
    """
    def start(self):
        """
        Performs any setup required before a stream is processed.
        """
        pass

    @abstractmethod
    def process_element(
            self,
            element: InputElementType,
            then: ThenFunction[OutputElementType],
            done: DoneFunction
    ):
        """
        Processes a single element in the stream.

        :param element:     The element to process.
        :param then:        A function to call to forward processed elements
                            further into the stream.
        :param done:        Should be called when no more processed elements will
                            be produced.
        """
        raise NotImplementedError(self.process_element.__qualname__)

    @abstractmethod
    def finish(
            self,
            then: ThenFunction[OutputElementType],
            done: DoneFunction
    ):
        """
        Called when no more elements will be passed to this processor.

        :param then:        A function to call to forward processed elements
                            further into the stream.
        :param done:        Should be called when no more processed elements will
                            be produced.
        """
        raise NotImplementedError(self.finish.__qualname__)
