from ..core import FormatSpecifier
from .convert import *
from .io import *


class TFFormatSpecifier(FormatSpecifier):
    """
    Specifier of the Tensorflow TFRecords format.
    """
    def __init__(self):
        super().__init__(
            TensorflowExampleReader,
            FromTensorflowExample,
            ToTensorflowExample,
            TensorflowExampleWriter
        )
