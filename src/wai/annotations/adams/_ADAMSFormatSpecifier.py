from ..core import FormatSpecifier
from .convert import *
from .io import *


class ADAMSFormatSpecifier(FormatSpecifier):
    """
    Specifier of the ADAMS format.
    """
    def __init__(self):
        super().__init__(
            ADAMSReportReader,
            FromADAMSReport,
            ToADAMSReport,
            ADAMSReportWriter
        )
