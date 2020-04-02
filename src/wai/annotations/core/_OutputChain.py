from typing import Iterable, Tuple, Iterator, IO

from .components import InternalFormatConverter, Writer
from .stream import InlineStreamProcessor
from ._InternalFormat import InternalFormat


class OutputChain:
    """
    Combines a writer and an internal format converter into
    a single unit for writing annotations in the internal format
    to disk.
    """
    def __init__(self, writer: Writer, converter: InternalFormatConverter, *pre_processors: InlineStreamProcessor):
        self._writer: Writer = writer
        self._converter: InternalFormatConverter = converter
        self._pre_processors: Tuple[InlineStreamProcessor] = pre_processors

    @property
    def writer(self) -> Writer:
        """
        Gets the writer.
        """
        return self._writer

    @property
    def converter(self) -> InternalFormatConverter:
        """
        Gets the internal format converter.
        """
        return self._converter

    @property
    def pre_processors(self) -> Tuple[InlineStreamProcessor]:
        """
        Gets the pre-processors.
        """
        return self._pre_processors

    def save(self, instances: Iterable[InternalFormat]):
        """
        Writes a series of instances to disk.

        :param instances:   The instances to write to disk.
        """
        # Apply the pre-processing
        for pre_processor in reversed(self._pre_processors):
            instances = pre_processor.process(instances)

        self._writer.save(self._converter.convert_all(instances))

    def file_iterator(self, instances: Iterable[InternalFormat]) -> Iterator[Tuple[str, IO[bytes]]]:
        """
        Converts a series of instances into the files they are written to.
        No files are actually written.

        N.B. Some files are written, but to a temporary directory which is
        removed on iterator completion.

        :param instances:   The instances to write.
        :return:            An iterator of filename, file-contents pairs.
        """
        # Apply the pre-processing
        for pre_processor in reversed(self._pre_processors):
            instances = pre_processor.process(instances)

        return self._writer.file_iterator(self._converter.convert_all(instances))
