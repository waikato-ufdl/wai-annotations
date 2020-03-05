"""
Module which configures the argument parser for the main function.
"""
from argparse import ArgumentParser

from ..core import Settings

# Import the components that are available to us
from ._components import (
    get_available_input_formats,
    get_available_output_formats,
    get_reader_factory,
    get_external_format_converter_factory,
    get_internal_format_converter_factory,
    get_writer_factory
)


def configure_input_parser(parser: ArgumentParser, format: str):
    """
    Configures an argument parser with the input options
    of a particular format.

    :param parser:  The parser to configure.
    :param format:  The input format to configure for.
    """
    get_reader_factory(format).configure_parser(parser)
    get_external_format_converter_factory(format).configure_parser(parser)


def configure_output_parser(parser: ArgumentParser, format: str):
    """
    Configures an argument parser with the output options
    of a particular format.

    :param parser:  The parser to configure.
    :param format:  The output format to configure for.
    """
    get_internal_format_converter_factory(format).configure_parser(parser)
    get_writer_factory(format).configure_parser(parser)


def get_main_parser() -> ArgumentParser:
    """
    Gets the argument parser for the main function.

    :return:    The parser.
    """
    # Create the unconfigured parser
    parser: ArgumentParser = ArgumentParser()

    # Add any global options
    Settings.configure_parser(parser)

    # Create a first level sub-parser set for selecting the input type
    input_subparsers = parser.add_subparsers(dest="input_type")

    # Add each available input type to the parser
    for input_format in get_available_input_formats():
        # Create a sub-parser for this input type
        input_subparser = input_subparsers.add_parser(input_format)

        # Configure the sub-parser using the components
        configure_input_parser(input_subparser, input_format)

        # Create a second level sub-parser set for selecting the output type
        output_subparsers = input_subparser.add_subparsers(dest="output_type")

        for output_format in get_available_output_formats():
            # Create a sub-parser for this output type
            output_subparser = output_subparsers.add_parser(output_format)

            # Configure the sub-parser using the components
            configure_output_parser(output_subparser, output_format)

    return parser
