"""
Contains the global debug flag for wai.annotations.
"""
# The global debug flag
__debug: bool = False


def get_debug() -> bool:
    """
    Gets the global debug flag for wai.annotations.

    :return:    The setting of the flag.
    """
    global __debug
    return __debug


def set_debug(value: bool):
    """
    Sets the global debug flag for wai.annotations.

    :param value:   The new setting for the flag.
    """
    global __debug
    __debug = value
