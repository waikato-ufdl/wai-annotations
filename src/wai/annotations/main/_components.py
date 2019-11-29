"""
Module defining the components available to the main function.
"""
from typing import Dict, Optional, Tuple, Type, Set

from ..core import Reader, ExternalFormatConverter, InternalFormatConverter, Writer
from ..converters import *
from ..io import *

# The type of a specification of the components for a single external format
ComponentSpec = Tuple[
    Optional[Type[Reader]],
    Optional[Type[ExternalFormatConverter]],
    Optional[Type[InternalFormatConverter]],
    Optional[Type[Writer]]
]

components: Dict[str, ComponentSpec] = {
    "adams": (ADAMSReportReader, FromADAMSReport, ToADAMSReport, ADAMSReportWriter),
    "tfrecords": (TensorflowExampleReader, FromTensorflowExample, ToTensorflowExample, TensorflowExampleWriter),
    "coco": (COCOReader, FromCOCO, ToCOCO, COCOWriter),
    "vgg": (VGGReader, FromVGG, ToVGG, VGGWriter),
    "roi": (ROIReader, FromROI, ToROI, ROIWriter)
}


def get_formats() -> Set[str]:
    """
    Gets the set of known format identifiers.
    """
    return set(components.keys())


def ensure_format(format: str):
    """
    Raises an error if the format is not known.

    :param format:  The format to check.
    """
    # Get the formats
    formats = get_formats()

    # Check the given format
    if format not in formats:
        raise ValueError(f"Unknown format '{format}'\n"
                         f"Available formats are {formats}")


def get_reader_class(format: str) -> Optional[Type[Reader]]:
    """
    Gets the reader class for a given format.

    :param format:  The format identifier.
    :return:        The reader class for the format.
    """
    # Check the format is known
    ensure_format(format)

    # Get the reader class for the format
    return components[format][0]


def get_external_format_converter_class(format: str) -> Optional[Type[ExternalFormatConverter]]:
    """
    Gets the external format converter class for a given format.

    :param format:  The format identifier.
    :return:        The external format converter class for the format.
    """
    # Check the format is known
    ensure_format(format)

    # Get the reader class for the format
    return components[format][1]


def get_internal_format_converter_class(format: str) -> Optional[Type[InternalFormatConverter]]:
    """
    Gets the internal format converter class for a given format.

    :param format:  The format identifier.
    :return:        The internal format converter class for the format.
    """
    # Check the format is known
    ensure_format(format)

    # Get the reader class for the format
    return components[format][2]


def get_writer_class(format: str) -> Optional[Type[Writer]]:
    """
    Gets the writer class for a given format.

    :param format:  The format identifier.
    :return:        The writer class for the format.
    """
    # Check the format is known
    ensure_format(format)

    # Get the reader class for the format
    return components[format][3]
