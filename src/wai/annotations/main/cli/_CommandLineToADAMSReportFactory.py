from typing import Type

from ...core.cli import CommandLineInternalFormatConverterFactory
from ...core import InternalFormatConverter


class CommandLineToADAMSReportFactory(CommandLineInternalFormatConverterFactory):
    """
    Command-line factory that produces ToADAMSReport converters.
    """
    @classmethod
    def related_class(cls) -> Type[InternalFormatConverter]:
        from ...adams.convert import ToADAMSReport
        return ToADAMSReport
