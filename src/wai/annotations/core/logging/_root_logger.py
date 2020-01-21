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
    return logging.getLogger(ROOT_LOGGER_NAME)
