"""
Module for the root logger for the wai.annotations library.
"""
import logging

# The name of the root logger
ROOT_LOGGER_NAME: str = "wai.annotations"


def get_library_root_logger() -> logging.Logger:
    """
    Gets the root logger for the library.

    :return:    The logger.
    """
    # Get the library root logger
    logger = logging.getLogger(ROOT_LOGGER_NAME)

    # Add a null handler to it so that applications not using logging
    # don't complain
    logger.addHandler(logging.NullHandler())

    return logger
