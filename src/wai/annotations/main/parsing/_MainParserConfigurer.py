from argparse import ArgumentParser
from logging import Logger
from typing import Optional, List, Tuple

from wai.common.cli import ArgumentParserConfigurer

from ...core import LibrarySettings, DimensionDiscarder, set_settings, InputChain, OutputChain
from ...core.plugin import registry
from .._MainSettings import MainSettings
from ._InputSideParserConfigurer import InputSideParserConfigurer
from ._OutputSideParserConfigurer import OutputSideParserConfigurer


class MainParserConfigurer(ArgumentParserConfigurer):
    """
    Configurer for the main argument parser.
    """
    def __init__(self, logger: Optional[Logger] = None, *, no_input: bool = False, no_output: bool = False):
        self._with_input: bool = not no_input
        self._with_output: bool = not no_output

        self._logger: Optional[Logger] = logger

    def configure_parser(self, parser: ArgumentParser):
        # Add library settings
        LibrarySettings.configure_parser(parser)

        # Add the main settings
        MainSettings.configure_parser(parser)

        # Add the dimension discarder
        DimensionDiscarder.configure_parser(parser)

        # Create an output-side configurer
        if self._with_output:
            output_configurer = OutputSideParserConfigurer()

            def configure_output(sub_parser, format):
                output_configurer.configure_parser(sub_parser)
        else:
            def configure_output(sub_parser, format):
                pass

        # Chain it with an input-side configurer
        if self._with_input:
            InputSideParserConfigurer(configure_output).configure_parser(parser)
        else:
            configure_output(parser, "")

    def parse(self, args: Optional[List[str]] = None) -> Tuple[MainSettings,
                                                               Optional[Tuple[str, InputChain]],
                                                               Optional[Tuple[str, OutputChain]]]:
        """
        Parses the arguments to the main function.

        :param args:    The command-line arguments.
        :return:        The main settings, and the configured processing
                        chains for the set sides (input/output).
        """
        # Parse the arguments
        parser = self.get_configured_parser()
        namespace = parser.parse_args(args)

        # Instantiate the settings
        set_settings(LibrarySettings(namespace))
        main_settings = MainSettings(namespace)

        # If we were given a logger, set its verbosity and log the namespace
        if self._logger is not None:
            self._logger.setLevel(main_settings.VERBOSITY)
            self._logger.debug(f"ARGS:\n" + "\n".join(f"{name}={value}" for name, value in vars(namespace).items()))

        # Create the internal-format processors
        internal_format_processors = (DimensionDiscarder(namespace),)
        coercion = main_settings.COERCION
        if coercion is not None:
            internal_format_processors = *internal_format_processors, coercion()

        # Process the input side arguments if specified
        parsed_input = None
        if self._with_input:
            # Make sure an input format was specified (currently no required flag for sub-parsers)
            if not hasattr(namespace, "input_type"):
                parser.error(f"No input type provided")

            # Get the input format
            input_format = namespace.input_type

            # Create the input chain
            input_chain = InputChain(
                registry.get_reader_factory(input_format).instantiate(namespace),
                registry.get_external_format_converter_factory(input_format).instantiate(namespace),
                *internal_format_processors
            )

            # Blank the internal format processors so they aren't used by the output side as well
            internal_format_processors = tuple()

            parsed_input = input_format, input_chain

        # Process the output side arguments if specified
        parsed_output = None
        if self._with_output:
            # Make sure an output format was specified (currently no required flag for sub-parsers)
            if not hasattr(namespace, "output_type"):
                parser.error(f"No output type provided")

            # Get the output format
            output_format = namespace.output_type

            # Create the output chain
            output_chain = OutputChain(
                registry.get_writer_factory(output_format).instantiate(namespace),
                registry.get_internal_format_converter_factory(output_format).instantiate(namespace),
                *reversed(internal_format_processors)
            )

            parsed_output = output_format, output_chain

        return main_settings, parsed_input, parsed_output
