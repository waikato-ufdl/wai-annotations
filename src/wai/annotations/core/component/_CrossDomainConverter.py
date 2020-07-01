from abc import abstractmethod
from typing import Generic, TypeVar, Iterator, Iterable

from wai.common.cli import CLIInstantiable

from ..instance import Instance

InputType = TypeVar("InputType", bound=Instance)
OutputType = TypeVar("OutputType", bound=Instance)


class CrossDomainConverter(CLIInstantiable, Generic[InputType, OutputType]):
    """
    Base class for cross-domain converters, which convert instances
    from one domain into another.
    """
    def convert(self, stream: Iterable[InputType]) -> Iterator[OutputType]:
        """
        Converts the stream.

        :param stream:  The stream to convert.
        :return:        The stream with processing.
        """
        # Process each element in turn
        for element in stream:
            # Process the element
            yield from self._convert_element(element)

    @abstractmethod
    def _convert_element(self, element: InputType) -> Iterable[OutputType]:
        """
        Processes a single element in the stream.

        :param element:     The element to process.
        :return:            The processed element.
        """
        pass
