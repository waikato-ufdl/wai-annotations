from typing import Type

from ...core.cli import CommandLineReaderFactory
from ...core import Reader


class CommandLineVGGReaderFactory(CommandLineReaderFactory):
    """
    Command-line factory that produces VGGReader readers.
    """
    @classmethod
    def related_class(cls) -> Type[Reader]:
        from ...vgg.io import VGGReader
        return VGGReader
