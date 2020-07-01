from typing import Iterator, TypeVar, Generic

from ..component import InputConverter, Reader
from ..instance import Instance

ExternalFormat = TypeVar("ExternalFormat")
InstanceType = TypeVar("InstanceType", bound=Instance)


class InputStage(Generic[ExternalFormat, InstanceType]):
    """
    Combines a reader and an input converter into
    a single unit for reading annotations files into the
    converter's domain.
    """
    def __init__(self, reader: Reader[ExternalFormat], converter: InputConverter[ExternalFormat, InstanceType]):
        self._reader: Reader[ExternalFormat] = reader
        self._converter: InputConverter[ExternalFormat, InstanceType] = converter

    @property
    def reader(self) -> Reader[ExternalFormat]:
        """
        Gets the reader.
        """
        return self._reader

    @property
    def converter(self) -> InputConverter[ExternalFormat, InstanceType]:
        """
        Gets the input converter.
        """
        return self._converter

    def load(self) -> Iterator[InstanceType]:
        """
        Reads annotations into the domain format.

        :return:    An iterator over the internal-format annotations.
        """
        return self._converter.convert_all(self._reader.load())
