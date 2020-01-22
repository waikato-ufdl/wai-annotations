from typing import Type

from ...core.cli import CommandLineReaderFactory
from ...core import Reader


class CommandLineROIReaderFactory(CommandLineReaderFactory):
    """
    Command-line factory that produces ROIReader readers.
    """
    @classmethod
    def related_class(cls) -> Type[Reader]:
        from ...roi.io import ROIReader
        return ROIReader
