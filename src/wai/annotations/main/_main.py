"""
Module containing the main entry point functions for converting annotations.
"""
import traceback
from typing import Optional

from wai.common.cli import OptionsList
from wai.common.logging import create_standard_application_root_logger, DEBUG_HANDLER_NAME

from ..core.builder import ConversionPipelineBuilder
from ._help import help_plugins, list_plugins, format_help, list_domains
from ._macros import perform_macro_expansion
from ._MainSettings import MainSettings


def main(options: Optional[OptionsList] = None):
    """
    Main function of the annotations converter.

    :param options:    The CLI arguments to the program.
    """
    # Setup logging
    logger = create_standard_application_root_logger()

    # Remove the PIL logging from the debug logger
    for handler in logger.handlers:
        if handler.name == DEBUG_HANDLER_NAME:
            handler.addFilter(lambda record: record.name != 'PIL.PngImagePlugin')

    # Get the command-line arguments if none are specified directly
    if options is None:
        import sys
        options = sys.argv[1:]

    # SPECIAL CASE: If --help-plugins is in the arguments, all arguments are considered global
    if "--help-plugins" in options:
        global_options, stage_options = options, []
    else:
        global_options, stage_options = ConversionPipelineBuilder.split_global_options(options)

    # Consume global options
    main_settings = MainSettings(global_options)
    logger.setLevel(main_settings.VERBOSITY)

    # If requested to provide general help, do so and exit
    if main_settings.HELP:
        print(format_help())
        return

    # If requested to list the plugins, do so and exit
    if main_settings.LIST_PLUGINS:
        print(list_plugins())
        return

    # If requested to list the domains, do so and exit
    if main_settings.LIST_DOMAINS:
        print(list_domains())
        return

    # If requested to print plugin help, do so and exit
    if main_settings.HELP_PLUGINS is not None:
        print(help_plugins(None if len(main_settings.HELP_PLUGINS) == 0 else set(main_settings.HELP_PLUGINS)))
        return

    # Perform macro expansion on the stage options
    stage_options = perform_macro_expansion(stage_options, main_settings.MACRO_FILE)

    # Create the conversion pipeline
    conversion_pipeline = ConversionPipelineBuilder.from_options(stage_options)

    # Log the to/from formats we are converting
    # TODO: Reinstate
    # logger.info(f"Converting from {input_format} to {output_format}")

    # Execute the pipeline
    conversion_pipeline.process()

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
