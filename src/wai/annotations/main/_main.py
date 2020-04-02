"""
Module containing the main entry point functions for converting annotations.
"""
import traceback
from typing import List, Optional

from wai.common.logging import create_standard_application_root_logger, DEBUG_HANDLER_NAME

from .parsing import MainParserConfigurer


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
    main_settings, input_side, output_side = MainParserConfigurer(logger).parse(args)
    assert input_side is not None
    input_format, input_chain = input_side
    assert output_side is not None
    output_format, output_chain = output_side

    # Log the to/from formats we are converting
    logger.info(f"Converting from {input_format} to {output_format}")

    # Apply the input chain to the output chain
    output_chain.save(input_chain.load())

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
