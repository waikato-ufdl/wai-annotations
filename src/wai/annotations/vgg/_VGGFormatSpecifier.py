from ..core import FormatSpecifier
from .convert import *
from .io import *


class VGGFormatSpecifier(FormatSpecifier):
    """
    Specifier of the VIA VGG format.
    """
    def __init__(self):
        super().__init__(
            VGGReader,
            FromVGG,
            ToVGG,
            VGGWriter
        )
