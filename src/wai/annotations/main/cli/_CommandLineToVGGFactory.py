from typing import Type

from ...core.cli import CommandLineInternalFormatConverterFactory
from ...core import InternalFormatConverter


class CommandLineToVGGFactory(CommandLineInternalFormatConverterFactory):
    """
    Command-line factory that produces ToVGG converters.
    """
    @classmethod
    def related_class(cls) -> Type[InternalFormatConverter]:
        from ...vgg.convert import ToVGG
        return ToVGG
