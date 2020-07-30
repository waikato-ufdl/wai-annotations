import os

from wai.common.config import get_config_dir


def get_default_macro_dir() -> str:
    """
    Gets the default directory to store macros in.

    :return:    The directory string.
    """
    # Get the system app configuration standard location
    config_dir = get_config_dir()

    # Define a folder for our configuration in the standard location
    default_macro_dir = os.path.join(config_dir, 'wai-annotations')

    # Make sure the location exists
    if not os.path.exists(default_macro_dir):
        os.mkdir(default_macro_dir)

    return default_macro_dir
