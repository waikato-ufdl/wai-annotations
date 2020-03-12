from wai.common.cli import CLIInstantiable
from wai.common.cli.options import TypedOption

from ._ImageFormat import ImageFormat


class LibrarySettings(CLIInstantiable):
    """
    The main settings class for the library. Contains global
    settings.
    """
    # The order of preference of image formats
    IMAGE_FORMAT_PREFERENCE_ORDER = TypedOption(
        "-e", "--extensions",
        type=ImageFormat,
        nargs=2,
        metavar="FORMAT",
        default=[ImageFormat.PNG, ImageFormat.JPG],
        help="image format extensions in order of preference"
    )


# The global settings instance (all settings default)
global_settings: LibrarySettings = LibrarySettings([])


def get_settings() -> LibrarySettings:
    """
    Gets the current settings. It is an error to call this before
    set_settings has been called.

    :return:    The current settings.
    """
    global global_settings
    return global_settings


def set_settings(settings: LibrarySettings):
    """
    Sets the settings.

    :param settings:   The settings to set.
    """
    global global_settings
    global_settings = settings
