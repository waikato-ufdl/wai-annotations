from typing import Iterable, Tuple, Iterator, IO, TypeVar, Generic

from ..component import OutputConverter, Writer, LocalWriter
from ..instance import Instance

ExternalFormat = TypeVar("ExternalFormat")
InstanceType = TypeVar("InstanceType", bound=Instance)


class OutputStage(Generic[InstanceType, ExternalFormat]):
    """
    Combines a writer and an output converter into
    a single unit for writing annotations in a domain format
    to disk.
    """
    def __init__(self, writer: Writer[ExternalFormat], converter: OutputConverter[InstanceType, ExternalFormat]):
        self._writer: Writer[ExternalFormat] = writer
        self._converter: OutputConverter[InstanceType, ExternalFormat] = converter

    @property
    def writer(self) -> Writer[ExternalFormat]:
        """
        Gets the writer.
        """
        return self._writer

    @property
    def converter(self) -> OutputConverter[InstanceType, ExternalFormat]:
        """
        Gets the output converter.
        """
        return self._converter

    def save(self, instances: Iterable[InstanceType]):
        """
        Writes a series of instances to disk.

        :param instances:   The instances to write to disk.
        """
        self._writer.save(self._converter.convert_all(instances))

    def file_iterator(self, instances: Iterable[InstanceType]) -> Iterator[Tuple[str, IO[bytes]]]:
        """
        Converts a series of instances into the files they are written to.
        No files are actually written.

        N.B. Some files are written, but to a temporary directory which is
        removed on iterator completion.

        :param instances:   The instances to write.
        :return:            An iterator of filename, file-contents pairs.
        """
        # Make sure the writer is capable of file iteration
        if not isinstance(self._writer, LocalWriter):
            raise TypeError(f"{self._writer.__class__.__name__} is not capable of file iteration")

        return self._writer.file_iterator(self._converter.convert_all(instances))
