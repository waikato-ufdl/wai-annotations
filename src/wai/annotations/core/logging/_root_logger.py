"""
Module for the root logger for the wai.annotations library.
"""
import logging

# The name of the root logger
# TODO: Make dynamically resolved
ROOT_LOGGER_NAME: str = "wai.annotations"

# The cached root logger
__root_logger: logging.Logger = logging.getLogger(ROOT_LOGGER_NAME)

# Add a null handler to it so that applications not using logging
# don't complain
__root_logger.addHandler(logging.NullHandler())


def get_library_root_logger() -> logging.Logger:
    """
    Gets the root logger for the library.

    :return:    The logger.
    """
    global __root_logger
    return __root_logger
