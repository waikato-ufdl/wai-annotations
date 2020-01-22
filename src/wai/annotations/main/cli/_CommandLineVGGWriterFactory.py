from typing import Type

from ...core.cli import CommandLineSeparateImageWriterFactory
from ...core import SeparateImageWriter


class CommandLineVGGWriterFactory(CommandLineSeparateImageWriterFactory):
    """
    Command-line factory that produces VGGWriter writers.
    """
    @classmethod
    def related_class(cls) -> Type[SeparateImageWriter]:
        from ...vgg.io import VGGWriter
        return VGGWriter

    @classmethod
    def output_help_text(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"
