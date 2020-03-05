from typing import Type

from .._JSONWriter import JSONWriter
from ._CommandLineJSONWriterFactory import CommandLineJSONWriterFactory


class CommandLineVGGWriterFactory(CommandLineJSONWriterFactory):
    """
    Command-line factory that produces VGGWriter writers.
    """
    @classmethod
    def related_class(cls) -> Type[JSONWriter]:
        from ...vgg.io import VGGWriter
        return VGGWriter

    @classmethod
    def output_help_text(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"
