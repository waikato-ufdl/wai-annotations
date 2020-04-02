from typing import Iterator, Tuple

from .components import ExternalFormatConverter, Reader
from .stream import InlineStreamProcessor
from ._InternalFormat import InternalFormat


class InputChain:
    """
    Combines a reader and an external format converter into
    a single unit for reading annotations files into the
    internal format.
    """
    def __init__(self, reader: Reader, converter: ExternalFormatConverter, *post_processors: InlineStreamProcessor):
        self._reader: Reader = reader
        self._converter: ExternalFormatConverter = converter
        self._post_processors: Tuple[InlineStreamProcessor] = post_processors

    @property
    def reader(self) -> Reader:
        """
        Gets the reader.
        """
        return self._reader

    @property
    def converter(self) -> ExternalFormatConverter:
        """
        Gets the external format converter.
        """
        return self._converter

    @property
    def post_processors(self) -> Tuple[InlineStreamProcessor]:
        """
        Gets the post-processors.
        """
        return self._post_processors

    def load(self) -> Iterator[InternalFormat]:
        """
        Reads annotations into the internal format.

        :return:    An iterator over the internal-format annotations.
        """
        # Create the input chain
        input_chain = self._converter.convert_all(self._reader.load())

        # Apply the post-processing
        for post_processor in self._post_processors:
            input_chain = post_processor.process(input_chain)

        return input_chain
