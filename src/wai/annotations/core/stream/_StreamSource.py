from abc import abstractmethod
from typing import Generic

from ._typing import ThenFunction, DoneFunction, ElementType


class StreamSource(Generic[ElementType]):
    """
    The source of elements in a stream.
    """
    @abstractmethod
    def produce(
            self,
            then: ThenFunction[ElementType],
            done: DoneFunction
    ):
        """
        Produces elements and inserts them into the stream. Should call 'then'
        for each element produced, and then call 'done' when finished.

        :param then:    A function which forwards elements into the stream.
        :param done:    A function which closes the stream when called.
        """
        raise NotImplementedError(self.produce.__qualname__)
