from typing import Iterator

from .components import ExternalFormatConverter, Reader
from ._InternalFormat import InternalFormat


class InputChain:
    """
    Combines a reader and an external format converter into
    a single unit for reading annotations files into the
    internal format.
    """
    def __init__(self, reader: Reader, converter: ExternalFormatConverter):
        self._reader: Reader = reader
        self._converter: ExternalFormatConverter = converter

    def load(self) -> Iterator[InternalFormat]:
        """
        Reads annotations into the internal format.

        :return:    An iterator over the internal-format annotations.
        """
        return self._converter.convert_all(self._reader.load())
