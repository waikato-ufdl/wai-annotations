"""
Module for the root logger for the wai.annotations library.
"""
import logging

from wai.common.logging import create_standard_library_root_logger

# The name of the root logger
# TODO: Make dynamically resolved
ROOT_LOGGER_NAME: str = "wai.annotations"

# The cached root logger
__root_logger: logging.Logger = create_standard_library_root_logger(ROOT_LOGGER_NAME)


def get_library_root_logger() -> logging.Logger:
    """
    Gets the root logger for the library.

    :return:    The logger.
    """
    global __root_logger
    return __root_logger
