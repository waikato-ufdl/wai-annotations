"""
Module defining the components available to the main function.
"""
from typing import Dict, Optional, Tuple, Type, Set

from ..core.cli import *

# The type of a specification of the components for a single external format
ComponentSpec = Tuple[
    Optional[Type[CommandLineReaderFactory]],
    Optional[Type[CommandLineExternalFormatConverterFactory]],
    Optional[Type[CommandLineInternalFormatConverterFactory]],
    Optional[Type[CommandLineWriterFactory]]
]

components: Dict[str, ComponentSpec] = {
    "adams": (CommandLineADAMSReportReaderFactory,
              CommandLineFromADAMSReportFactory,
              CommandLineToADAMSReportFactory,
              CommandLineADAMSReportWriterFactory),
    "coco": (CommandLineCOCOReaderFactory,
             CommandLineFromCOCOFactory,
             CommandLineToCOCOFactory,
             CommandLineCOCOWriterFactory),
    "roi": (CommandLineROIReaderFactory,
            CommandLineFromROIFactory,
            CommandLineToROIFactory,
            CommandLineROIWriterFactory),
    "tfrecords": (CommandLineTensorflowExampleReaderFactory,
                  CommandLineFromTensorflowExampleFactory,
                  CommandLineToTensorflowExampleFactory,
                  CommandLineTensorflowExampleWriterFactory),
    "vgg": (CommandLineVGGReaderFactory,
            CommandLineFromVGGFactory,
            CommandLineToVGGFactory,
            CommandLineVGGWriterFactory)
}


def get_formats() -> Set[str]:
    """
    Gets the set of known format identifiers.
    """
    return set(components.keys())


def ensure_format(format: str, input: Optional[bool] = None):
    """
    Raises an error if the format is not known.

    :param format:  The format to check.
    :param input:   True to check the format can be read,
                    False to check the format can be written,
                    None (the default) to check both.
    """
    # Get the formats
    formats = get_formats()

    # Check the given format exists at all
    if format not in formats:
        raise ValueError(f"Unknown format '{format}'. Available formats are {formats}")

    # Get the components to check for existence
    components_to_check = (components[format] if input is None else
                           components[format][:2] if input else
                           components[format][2:])

    if any(component is None for component in components_to_check):
        check_string = ("readable/writable" if input is None else
                        "readable" if input else
                        "writable")
        raise ValueError(f"Format '{format}' is not currently implemented as a "
                         f"{check_string} format")


def get_reader_factory(format: str) -> Optional[Type[CommandLineReaderFactory]]:
    """
    Gets the reader factory for a given format.

    :param format:  The format identifier.
    :return:        The reader factory for the format.
    """
    # Check the format is known
    ensure_format(format, True)

    # Get the reader factory for the format
    return components[format][0]


def get_external_format_converter_factory(format: str) -> Optional[Type[CommandLineExternalFormatConverterFactory]]:
    """
    Gets the external format converter factory for a given format.

    :param format:  The format identifier.
    :return:        The external format converter factory for the format.
    """
    # Check the format is known
    ensure_format(format, True)

    # Get the external format converter factory for the format
    return components[format][1]


def get_internal_format_converter_factory(format: str) -> Optional[Type[CommandLineInternalFormatConverterFactory]]:
    """
    Gets the internal format converter factory for a given format.

    :param format:  The format identifier.
    :return:        The internal format converter factory for the format.
    """
    # Check the format is known
    ensure_format(format, False)

    # Get the internal format converter factory for the format
    return components[format][2]


def get_writer_factory(format: str) -> Optional[Type[CommandLineWriterFactory]]:
    """
    Gets the writer factory for a given format.

    :param format:  The format identifier.
    :return:        The writer factory for the format.
    """
    # Check the format is known
    ensure_format(format, False)

    # Get the reader factory for the format
    return components[format][3]
