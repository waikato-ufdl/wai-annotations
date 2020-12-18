"""
Module containing the main entry point functions for wai.annotations.
"""
import traceback
from typing import Optional

from wai.common.cli import OptionsList

from .commands import get_command_main
from .logging import get_app_logger
from ._help import main_help


def main(options: Optional[OptionsList] = None):
    """
    Main function of the annotations converter.

    :param options:    The CLI arguments to the program.
    """
    # Get the application logger
    logger = get_app_logger()

    # Get the command-line arguments if none are specified directly
    if options is None:
        import sys
        options = sys.argv[1:]

    if len(options) == 0:
        logger.warning("No command specified")
        print(main_help())
        return

    # Split the top-level command from the options
    command, command_options = options[0], options[1:]
    logger.info(f"command = {command}")
    if len(command_options) > 0:
        logger.info("command_options = \"" + "\", \"".join(command_options) + "\"")
    else:
        logger.info("command_options empty")

    # If the command is help, print the help
    if command in {"help", "-h", "--help"}:
        print(main_help())
        return

    try:
        command_main = get_command_main(command)
    except:
        logger.error(f"Unknown command '{command}'")
        print(main_help())
        return

    # Run the command
    command_main(command_options)


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
