from typing import Type

from ...core.cli import CommandLineReaderFactory
from ...core import Reader


class CommandLineCOCOReaderFactory(CommandLineReaderFactory):
    """
    Command-line factory that produces COCOReader readers.
    """
    @classmethod
    def related_class(cls) -> Type[Reader]:
        from ...coco.io import COCOReader
        return COCOReader
