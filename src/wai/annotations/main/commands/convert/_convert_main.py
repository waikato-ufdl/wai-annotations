"""
Module containing the main entry point function for converting annotations.
"""
from typing import Optional

from wai.common.cli import OptionsList

from ....core.builder import ConversionPipelineBuilder
from ...logging import get_app_logger
from ..plugins import PluginsOptions, get_plugins_formatted
from ._help import convert_help
from ._macros import perform_macro_expansion
from ._ConvertOptions import ConvertOptions


def convert_main(options: Optional[OptionsList] = None):
    """
    Main function for performing annotations conversion.

    :param options:
                The CLI arguments to the program.
    """
    # Get the application logger
    logger = get_app_logger()

    # Get the command-line arguments if none are specified directly
    if options is None:
        import sys
        options = sys.argv[1:]

    # Split the options into global and stage-specific
    global_options, stage_options = ConversionPipelineBuilder.split_global_options(options)

    # Consume global options
    try:
        convert_options = ConvertOptions(global_options)
    except ValueError:
        logger.exception("Error parsing convert options")
        print(convert_help())
        raise

    # Set the logger level from the options
    logger.setLevel(convert_options.VERBOSITY)

    # If the global help is requested, print it and return
    if convert_options.HELP:
        print(convert_help())
        return

    # If the last option is a call for help, provided help on the last stage
    if stage_options[-1] in ("-h", "--help"):
        # Get the last stage
        stage = ConversionPipelineBuilder.split_options(stage_options)[-1][0]

        # Set up options to format the help for the stage
        stage_plugin_options = PluginsOptions(["-o", stage, "-g"])

        # Print the help and exit
        print(get_plugins_formatted(stage_plugin_options))
        return

    # Perform macro expansion on the stage options
    stage_options = perform_macro_expansion(stage_options, convert_options.MACRO_FILE)

    # Create the conversion pipeline
    conversion_pipeline = ConversionPipelineBuilder.from_options(stage_options)

    # Execute the pipeline
    conversion_pipeline.process()

    logger.info("Finished conversion")
