"""
Logging actions for the main function.
"""
import logging
import sys
from typing import Optional

# The main logger
main_logger: Optional[logging.Logger] = None


def get_main_logger() -> logging.Logger:
    """
    Sets up the logger for the main function and returns
    it. Subsequent calls will return the same logger.

    :return:    The logger.
    """
    global main_logger

    # Setup the main logger if not already
    if main_logger is None:
        # Get the root logger
        main_logger = logging.getLogger()

        # Create a debug handler to print debug info to std-out
        debug_handler = logging.StreamHandler(sys.stdout)
        debug_handler.addFilter(
            lambda record: record.levelno == logging.DEBUG
        )
        debug_handler.setLevel(1)
        debug_handler.setFormatter(logging.Formatter("##DEBUG## {name} {created} - {pathname} - {funcName} - {message}",
                                                     style="{"))

        # Create a handler to print info messages to std-out
        info_handler = logging.StreamHandler(sys.stdout)
        info_handler.addFilter(lambda record: record.levelno == logging.INFO)
        info_handler.setFormatter(logging.Formatter("{asctime} - {message}",
                                                    style="{"))

        # Another handler to print all other message to std-err
        err_handler = logging.StreamHandler()
        err_handler.setLevel(logging.WARNING)
        err_handler.setFormatter(logging.Formatter("{levelname} {asctime} - {message}",
                                                   style="{"))

        # Add the handlers to the logger
        main_logger.addHandler(debug_handler)
        main_logger.addHandler(info_handler)
        main_logger.addHandler(err_handler)

        # Set the main logger to debug level
        main_logger.setLevel(logging.WARNING)

        # Remove unwanted 3rd-party logging
        debug_handler.addFilter(lambda record: record.name != 'PIL.PngImagePlugin')

    return main_logger
