from argparse import ArgumentParser, Namespace
from typing import Tuple, Dict, Any, Optional

from .coercions import Coercion, BoxBoundsCoercion, MaskBoundsCoercion
from ._ImageFormat import ImageFormat


class Settings:
    """
    The main settings class for the library. Contains global
    settings.
    """
    # The verbosity of logging to implement
    VERBOSITY: int = property(lambda self: self._verbosity)

    # The order of preference of image formats
    IMAGE_FORMAT_PREFERENCE_ORDER: Tuple[ImageFormat, ...] = property(lambda self: self._image_format_preference_order)

    # The coercion to apply to annotations
    COERCION: Optional[Coercion] = property(lambda self: self._coercion)

    def __init__(self,
                 verbosity: Optional[int] = None,
                 image_format_preference_order: Optional[Tuple[ImageFormat, ...]] = None,
                 force: Optional[Coercion] = None):
        super().__init__()

        self._verbosity: int = verbosity if verbosity is not None else 10
        self._image_format_preference_order: Tuple[ImageFormat, ...] = image_format_preference_order \
            if image_format_preference_order is not None else (ImageFormat.PNG, ImageFormat.JPG)
        self._coercion: Optional[Coercion] = force

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument(
            "-v", action="count", dest="verbosity", required=False,
            help="whether to be more verbose when generating the records")

        parser.add_argument(
            "-f", "--force", dest="force", required=False, choices=["bbox", "mask"],
            help="forces located objects into a particular boundary type"
        )

        parser.add_argument(
            "-e", "--extensions", dest="extensions", required=False,
            help="image format extensions in order of preference"
        )

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        return dict(
            verbosity=(cls._parse_verbosity(namespace.verbosity)
                       if namespace.verbosity is not None else None),
            image_format_preference_order=(cls._parse_extensions(namespace.extensions)
                                           if namespace.extensions is not None else None),
            force=(cls._parse_force(namespace.force)
                   if namespace.force is not None else None)
        )

    @classmethod
    def instance_from_namespace(cls, namespace: Namespace) -> 'Settings':
        return cls(**cls.determine_kwargs_from_namespace(namespace))

    @classmethod
    def _parse_verbosity(cls, value: int) -> int:
        """
        Parses the --verbosity option.

        :param value:   The integer count of the number of times the option was specified.
        :return:        The verbosity value.
        """
        return value * 10

    @classmethod
    def _parse_extensions(cls, value: str) -> Tuple[ImageFormat, ...]:
        """
        Parses the --extensions option.

        :param value:   The string value given at the command line.
        :return:        The image format preference order.
        """
        # Split the string into the individual formats
        format_strings = value.split(",")

        # Parse the format strings
        parsed_formats = tuple(map(ImageFormat.for_extension, format_strings))

        # Make sure all formats were recognised
        for parsed_format, format_string in zip(parsed_formats, format_strings):
            if parsed_format is None:
                raise ValueError(f"Image format preference order contains unrecognised "
                                 f"format '{format_string}'")

        # Make sure there are no duplicate formats
        seen = set()
        for parsed_format in parsed_formats:
            if parsed_format in seen:
                raise ValueError(f"Image format preference order contains duplicate specification "
                                 f"of '{parsed_format}' format")
            seen.add(parsed_format)

        return parsed_formats

    @classmethod
    def _parse_force(cls, value: str) -> Optional[Coercion]:
        """
        Parses the --force option.

        :param value:   The string value given at the command line.
        :return:        The (possible) coercion.
        """
        if value == "bbox":
            return BoxBoundsCoercion()
        elif value == "mask":
            return MaskBoundsCoercion()

        raise ValueError(f"Unrecognised value for force: {value}")


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
