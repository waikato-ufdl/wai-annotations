from typing import Type

from ...core.cli import CommandLineSeparateImageWriterFactory
from ...core import SeparateImageWriter


class CommandLineADAMSReportWriterFactory(CommandLineSeparateImageWriterFactory):
    """
    Command-line factory that produces ADAMSReportWriter writers.
    """
    @classmethod
    def related_class(cls) -> Type[SeparateImageWriter]:
        from ...adams.io import ADAMSReportWriter
        return ADAMSReportWriter

    @classmethod
    def output_help_text(cls) -> str:
        return "output directory to write files to"
