"""
Module containing the main entry point functions for converting annotations.
"""
import traceback
from typing import List, Optional

from wai.common.logging import create_standard_application_root_logger, DEBUG_HANDLER_NAME

from ..core import LibrarySettings, set_settings, DimensionDiscarder
from ..core.plugin import registry
from ._MainParserConfigurer import MainParserConfigurer
from ._MainSettings import MainSettings


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
    parser = MainParserConfigurer.get_configured_parser()
    namespace = parser.parse_args(args)

    # Set any global options
    set_settings(LibrarySettings(namespace))
    main_settings = MainSettings(namespace)

    # Set the logger verbosity from the arguments
    logger.setLevel(main_settings.VERBOSITY)

    logger.debug(f"ARGS:\n" + "\n".join(f"{name}={value}" for name, value in vars(namespace).items()))

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
    reader = registry.get_reader_factory(input_format).instantiate(namespace)
    input_converter = registry.get_external_format_converter_factory(input_format).instantiate(namespace)
    output_converter = registry.get_internal_format_converter_factory(output_format).instantiate(namespace)
    writer = registry.get_writer_factory(output_format).instantiate(namespace)

    # Create the input chain
    input_chain = input_converter.convert_all(reader.load())

    # Discard any annotations that don't meet the dimension requirements
    input_chain = DimensionDiscarder(namespace).process(input_chain)

    # Add a coercion if specified
    coercion = main_settings.COERCION
    if coercion is not None:
        input_chain = coercion().process(input_chain)

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
