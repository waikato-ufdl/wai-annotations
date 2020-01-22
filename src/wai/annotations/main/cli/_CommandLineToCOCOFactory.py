from typing import Type

from ...core.cli import CommandLineInternalFormatConverterFactory
from ...core import InternalFormatConverter


class CommandLineToCOCOFactory(CommandLineInternalFormatConverterFactory):
    """
    Command-line factory that produces ToCOCO converters.
    """
    @classmethod
    def related_class(cls) -> Type[InternalFormatConverter]:
        from ...coco.convert import ToCOCO
        return ToCOCO
