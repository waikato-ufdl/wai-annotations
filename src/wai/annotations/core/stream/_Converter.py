from abc import abstractmethod
from typing import Generic, Iterable, Iterator, TypeVar

# The types that the converter converts from and to
FromFormat = TypeVar("FromFormat")
ToFormat = TypeVar("ToFormat")


class Converter(Generic[FromFormat, ToFormat]):
    """
    Base class for converters.
    """
    def convert_all(self, instances: Iterable[FromFormat]) -> Iterator[ToFormat]:
        """
        Converts a series of instances.

        :param instances:   The instances in input format.
        :return:            The instances in output format.
        """
        for instance in instances:
            yield from self.convert(instance)

    @abstractmethod
    def convert(self, instance: FromFormat) -> Iterator[ToFormat]:
        """
        Converts an instance in input format into the output format.

        :param instance:    The instance in input format.
        :return:            The instance in output format.
        """
        pass
