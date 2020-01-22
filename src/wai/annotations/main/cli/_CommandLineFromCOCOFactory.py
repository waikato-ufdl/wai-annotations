from typing import Type

from ...core.cli import CommandLineExternalFormatConverterFactory
from ...core import ExternalFormatConverter


class CommandLineFromCOCOFactory(CommandLineExternalFormatConverterFactory):
    """
    Command-line factory that produces FromCOCO converters.
    """
    @classmethod
    def related_class(cls) -> Type[ExternalFormatConverter]:
        from ...coco.convert import FromCOCO
        return FromCOCO
