from typing import Type

from ...core.cli import CommandLineReaderFactory
from ...core import Reader


class CommandLineADAMSReportReaderFactory(CommandLineReaderFactory):
    """
    Command-line factory that produces ADAMSReportReader readers.
    """
    @classmethod
    def related_class(cls) -> Type[Reader]:
        from ...adams.io import ADAMSReportReader
        return ADAMSReportReader
