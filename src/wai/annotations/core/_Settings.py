from logging import WARNING, INFO, DEBUG
from typing import Optional

from wai.common import ClassRegistry
from wai.common.cli import CLIInstantiable
from wai.common.cli.options import CountOption, TypedOption, FlagOption, ClassOption
from wai.common.cli.util import TranslationTable

from .coercions import MaskBoundsCoercion, BoxBoundsCoercion
from ._ImageFormat import ImageFormat


class Settings(CLIInstantiable):
    """
    The main settings class for the library. Contains global
    settings.
    """
    # The verbosity of logging to implement
    VERBOSITY = CountOption(
        "-v",
        translation=TranslationTable(WARNING, INFO, DEBUG),
        help="whether to be more verbose when generating the records"
    )

    # The order of preference of image formats
    IMAGE_FORMAT_PREFERENCE_ORDER = TypedOption(
        "-e", "--extensions",
        type=ImageFormat,
        nargs=2,
        metavar="FORMAT",
        default=[ImageFormat.PNG, ImageFormat.JPG],
        help="image format extensions in order of preference"
    )

    # The coercion to apply to annotations
    COERCION = ClassOption(
        "-f", "--force",
        registry=ClassRegistry().alias(MaskBoundsCoercion, "mask").alias(BoxBoundsCoercion, "bbox"),
        help="forces located objects into a particular boundary type"
    )

    # Whether to include zero-area annotations
    INCLUDE_ZERO_AREA = FlagOption(
        "--include-zero-area",
        help="whether to process annotations which have zero width/height (excluded by default)"
    )


# The global settings instance
global_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Gets the current settings. It is an error to call this before
    set_settings has been called.

    :return:    The current settings.
    """
    global global_settings
    return global_settings


def set_settings(settings: Settings):
    """
    Sets the settings.

    :param settings:   The settings to set.
    """
    global global_settings
    global_settings = settings
