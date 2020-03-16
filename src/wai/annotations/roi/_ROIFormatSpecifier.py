from ..core import FormatSpecifier
from .convert import *
from .io import *


class ROIFormatSpecifier(FormatSpecifier):
    """
    Specifier of the ROI CSV format.
    """
    def __init__(self):
        super().__init__(
            ROIReader,
            FromROI,
            ToROI,
            ROIWriter
        )
