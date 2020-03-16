from ..core import FormatSpecifier
from .convert import *
from .io import *


class COCOFormatSpecifier(FormatSpecifier):
    """
    Specifier of the MS-COCO format.
    """
    def __init__(self):
        super().__init__(
            COCOReader,
            FromCOCO,
            ToCOCO,
            COCOWriter
        )
