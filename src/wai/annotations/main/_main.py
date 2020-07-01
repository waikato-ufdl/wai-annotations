"""
Module containing the main entry point functions for converting annotations.
"""
import traceback
from typing import Optional

from wai.common.cli import OptionsList
from wai.common.logging import create_standard_application_root_logger, DEBUG_HANDLER_NAME

from ..core.chain import ConversionChain
from ._list_plugins import list_plugins
from ._MainSettings import MainSettings


def main(options: Optional[OptionsList] = None):
    """
    Main function of the annotations converter.

    :param options:    The CLI arguments to the program.
    """
    # Setup logging
    logger = create_standard_application_root_logger()
    for handler in logger.handlers:
        if handler.name == DEBUG_HANDLER_NAME:
            handler.addFilter(lambda record: record.name != 'PIL.PngImagePlugin')

    # Get the command-line arguments if none are specified directly
    if options is None:
        import sys
        options = sys.argv[1:]

    # Pre-parse the command-line arguments
    global_options, stage_options = ConversionChain.split_global_options(options)

    # Consume global options
    main_settings = MainSettings(global_options)
    logger.setLevel(main_settings.VERBOSITY)

    # If requested to list the plugins, do so and exit
    if main_settings.LIST_PLUGINS:
        print(list_plugins())
        return

    # Create the conversion chain
    conversion_chain = ConversionChain.from_options(stage_options)

    # Log the to/from formats we are converting
    # TODO: Reinstate
    # logger.info(f"Converting from {input_format} to {output_format}")

    # Execute the chain
    conversion_chain.save()

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
