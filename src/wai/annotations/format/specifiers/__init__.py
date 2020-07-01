"""
Package for built-in format specifiers, so they can be loaded without loading
the dependencies of the formats.
"""
from ._ADAMSInputFormatSpecifier import ADAMSInputFormatSpecifier
from ._ADAMSOutputFormatSpecifier import ADAMSOutputFormatSpecifier

from ._COCOInputFormatSpecifier import COCOInputFormatSpecifier
from ._COCOOutputFormatSpecifier import COCOOutputFormatSpecifier

from ._ROIInputFormatSpecifier import ROIInputFormatSpecifier
from ._ROIOutputFormatSpecifier import ROIOutputFormatSpecifier

from ._TFRecordsInputFormatSpecifier import TFRecordsInputFormatSpecifier
from ._TFRecordsOutputFormatSpecifier import TFRecordsOutputFormatSpecifier

from ._VGGInputFormatSpecifier import VGGInputFormatSpecifier
from ._VGGOutputFormatSpecifier import VGGOutputFormatSpecifier
