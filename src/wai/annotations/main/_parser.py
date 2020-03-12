"""
Module which configures the argument parser for the main function.
"""
from argparse import ArgumentParser

from wai.common.cli import ArgumentParserConfigurer

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


class MainParserConfigurer(ArgumentParserConfigurer):
    """
    Configurer for the main argument parser.
    """
    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        # Add library settings
        Settings.configure_parser(parser)

        # Create a first level sub-parser set for selecting the input type
        input_subparsers = parser.add_subparsers(dest="input_type")

        # Add each available input type to the parser
        for input_format in get_available_input_formats():
            # Create a sub-parser for this input type
            input_subparser = input_subparsers.add_parser(input_format)

            # Configure the sub-parser using the components
            cls.configure_input_parser(input_subparser, input_format)

            # Create a second level sub-parser set for selecting the output type
            output_subparsers = input_subparser.add_subparsers(dest="output_type")

            for output_format in get_available_output_formats():
                # Create a sub-parser for this output type
                output_subparser = output_subparsers.add_parser(output_format)

                # Configure the sub-parser using the components
                cls.configure_output_parser(output_subparser, output_format)

    @classmethod
    def configure_input_parser(cls, parser: ArgumentParser, format: str):
        """
        Configures an argument parser with the input options
        of a particular format.

        :param parser:  The parser to configure.
        :param format:  The input format to configure for.
        """
        get_reader_factory(format).configure_parser(parser)
        get_external_format_converter_factory(format).configure_parser(parser)

    @classmethod
    def configure_output_parser(cls, parser: ArgumentParser, format: str):
        """
        Configures an argument parser with the output options
        of a particular format.

        :param parser:  The parser to configure.
        :param format:  The output format to configure for.
        """
        get_internal_format_converter_factory(format).configure_parser(parser)
        get_writer_factory(format).configure_parser(parser)
