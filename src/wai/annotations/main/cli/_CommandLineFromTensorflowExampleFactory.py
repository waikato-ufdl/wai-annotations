from typing import Type

from ...core.cli import CommandLineExternalFormatConverterFactory
from ...core import ExternalFormatConverter


class CommandLineFromTensorflowExampleFactory(CommandLineExternalFormatConverterFactory):
    """
    Command-line factory that produces FromTensorflowExample converters.
    """
    @classmethod
    def related_class(cls) -> Type[ExternalFormatConverter]:
        from ...tf.convert import FromTensorflowExample
        return FromTensorflowExample
