from argparse import ArgumentParser
from typing import Callable

from wai.common.cli import ArgumentParserConfigurer

from ...core.plugin import registry


class OutputSideParserConfigurer(ArgumentParserConfigurer):
    """
    Configures a parser for the input formats.
    """
    def __init__(self, sub_parser_hook: Callable[[ArgumentParser, str], None] = lambda sub_parser, format: None):
        self._sub_parser_hook: Callable[[ArgumentParser, str], None] = sub_parser_hook

    def configure_parser(self, parser: ArgumentParser):
        # Create a sub-parser set for selecting the output type
        output_subparsers = parser.add_subparsers(dest="output_type")

        # Add each available output type to the parser
        for output_format in registry.get_available_output_formats():
            # Create a sub-parser for this output type
            output_subparser = output_subparsers.add_parser(output_format)

            # Configure the sub-parser using the components
            registry.get_internal_format_converter_factory(output_format).configure_parser(output_subparser)
            registry.get_writer_factory(output_format).configure_parser(output_subparser)

            # Run the hook for this format
            self._sub_parser_hook(output_subparser, output_format)
