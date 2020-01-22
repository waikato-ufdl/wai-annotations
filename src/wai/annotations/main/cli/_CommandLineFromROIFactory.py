from typing import Type

from ...core.cli import CommandLineExternalFormatConverterFactory
from ...core import ExternalFormatConverter


class CommandLineFromROIFactory(CommandLineExternalFormatConverterFactory):
    """
    Command-line factory that produces FromROI converters.
    """
    @classmethod
    def related_class(cls) -> Type[ExternalFormatConverter]:
        from ...roi.convert import FromROI
        return FromROI
