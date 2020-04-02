from argparse import ArgumentParser
from typing import Callable

from wai.common.cli import ArgumentParserConfigurer

from ...core.plugin import registry


class InputSideParserConfigurer(ArgumentParserConfigurer):
    """
    Configures a parser for the input formats.
    """
    def __init__(self, sub_parser_hook: Callable[[ArgumentParser, str], None] = lambda sub_parser, format: None):
        self._sub_parser_hook: Callable[[ArgumentParser, str], None] = sub_parser_hook

    def configure_parser(self, parser: ArgumentParser):
        # Create a sub-parser set for selecting the input type
        input_subparsers = parser.add_subparsers(dest="input_type")

        # Add each available input type to the parser
        for input_format in registry.get_available_input_formats():
            # Create a sub-parser for this input type
            input_subparser = input_subparsers.add_parser(input_format)

            # Configure the sub-parser using the components
            registry.get_reader_factory(input_format).configure_parser(input_subparser)
            registry.get_external_format_converter_factory(input_format).configure_parser(input_subparser)

            # Run the hook for this format
            self._sub_parser_hook(input_subparser, input_format)
