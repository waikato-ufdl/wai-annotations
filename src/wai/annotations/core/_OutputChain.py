from typing import Iterable, Tuple

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
        Writes the instances to disk.

        :param instances:   An iterator over the internal-format annotations.
        """
        # Apply the pre-processing
        for pre_processor in reversed(self._pre_processors):
            instances = pre_processor.process(instances)

        self._writer.save(self._converter.convert_all(instances))
