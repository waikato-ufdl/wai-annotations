from typing import Type

from ...core.cli import CommandLineReaderFactory
from ...core import Reader


class CommandLineTensorflowExampleReaderFactory(CommandLineReaderFactory):
    """
    Command-line factory that produces TensorflowExampleReader readers.
    """
    @classmethod
    def related_class(cls) -> Type[Reader]:
        from ...tf.io import TensorflowExampleReader
        return TensorflowExampleReader
