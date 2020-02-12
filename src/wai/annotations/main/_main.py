"""
Module containing the main entry point functions for converting annotations.
"""
import logging
import traceback
from typing import List, Optional

from wai.common.logging import create_standard_application_root_logger, DEBUG_HANDLER_NAME

from ..core import Settings, get_settings, set_settings
from ._components import (
    get_reader_factory,
    get_external_format_converter_factory,
    get_internal_format_converter_factory,
    get_writer_factory
)
from ._parser import parser


def main(args: Optional[List[str]] = None):
    """
    Main function of the annotations converter.

    :param args:    The CLI arguments to the program.
    """
    # Setup logging
    logger = create_standard_application_root_logger()
    for handler in logger.handlers:
        if handler.name == DEBUG_HANDLER_NAME:
            handler.addFilter(lambda record: record.name != 'PIL.PngImagePlugin')

    # Parse the arguments
    namespace = parser.parse_args(args)

    # Set the logger verbosity from the arguments
    if namespace.verbosity == 1:
        logger.setLevel(logging.INFO)
    elif namespace.verbosity is not None:
        logger.setLevel(logging.DEBUG)

    logger.debug(f"ARGS:\n" + "\n".join(f"{name}={value}" for name, value in vars(namespace).items()))

    # Set any global options
    set_settings(Settings.instance_from_namespace(namespace))

    # Make sure an input and output format were specified
    # (currently no required flag for sub-parsers)
    if not hasattr(namespace, "input_type"):
        parser.error(f"No input type provided")
    elif not hasattr(namespace, "output_type"):
        parser.error(f"No output type provided")

    # Get the input and output formats
    input_format = namespace.input_type
    output_format = namespace.output_type

    logger.info(f"Converting from {input_format} to {output_format}")

    # Instantiate the components from the provided arguments
    reader = get_reader_factory(input_format).instance_from_namespace(namespace)
    input_converter = get_external_format_converter_factory(input_format).instance_from_namespace(namespace)
    output_converter = get_internal_format_converter_factory(output_format).instance_from_namespace(namespace)
    writer = get_writer_factory(output_format).instance_from_namespace(namespace)

    # Create the input chain
    input_chain = input_converter.convert_all(reader.load())

    # Add a coercion if specified
    if get_settings().COERCION is not None:
        input_chain = get_settings().COERCION.process(input_chain)

    # Finish the chain with the output components
    writer.save(output_converter.convert_all(input_chain))

    logger.info("Finished conversion")


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return:    0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1
