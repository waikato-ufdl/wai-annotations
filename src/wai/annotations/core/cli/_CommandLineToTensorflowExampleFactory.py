from typing import Type

from ...core.cli import CommandLineInternalFormatConverterFactory
from ...core import InternalFormatConverter


class CommandLineToTensorflowExampleFactory(CommandLineInternalFormatConverterFactory):
    """
    Command-line factory that produces toTensorflowExample converters.
    """
    @classmethod
    def related_class(cls) -> Type[InternalFormatConverter]:
        from ...tf.convert import ToTensorflowExample
        return ToTensorflowExample
