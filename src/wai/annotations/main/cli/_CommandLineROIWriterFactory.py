from typing import Type

from ...core.cli import CommandLineSeparateImageWriterFactory
from ...core import SeparateImageWriter


class CommandLineROIWriterFactory(CommandLineSeparateImageWriterFactory):
    """
    Command-line factory that produces ROIWriter writers.
    """
    @classmethod
    def related_class(cls) -> Type[SeparateImageWriter]:
        from ...roi.io import ROIWriter
        return ROIWriter

    @classmethod
    def output_help_text(cls) -> str:
        return "output directory to write files to"
