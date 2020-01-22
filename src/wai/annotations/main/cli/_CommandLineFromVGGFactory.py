from typing import Type

from ...core.cli import CommandLineExternalFormatConverterFactory
from ...core import ExternalFormatConverter


class CommandLineFromVGGFactory(CommandLineExternalFormatConverterFactory):
    """
    Command-line factory that produces FromVGG converters.
    """
    @classmethod
    def related_class(cls) -> Type[ExternalFormatConverter]:
        from ...vgg.convert import FromVGG
        return FromVGG
