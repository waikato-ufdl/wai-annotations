import os
from enum import Enum
from typing import Optional
from itertools import chain

from wai.common.cli import CLIRepresentable


class ImageFormat(CLIRepresentable, Enum):
    """
    Class enumerating the types of images we can work with. Each enumeration's
    value is a tuple of possible file extensions for that image type.
    """
    JPG = {"jpg", "JPG", "jpeg", "JPEG"}
    PNG = {"png", "PNG"}

    @classmethod
    def for_filename(cls, filename: str) -> Optional["ImageFormat"]:
        """
        Gets the image format for a given image filename.

        :param filename:    The image filename.
        :return:            The image format, or none if no format matched.
        """
        # Get the extension from the filename
        extension: str = os.path.splitext(filename)[1][1:]

        # Search for a format with this extension
        image_format = cls.for_extension(extension)

        # If a format was found, return it
        if image_format is not None:
            return image_format

        # Otherwise it is an error
        raise ValueError(f"'{filename}' does not end in a recognised extension "
                         f"({', '.join(chain(*(image_format.value for image_format in ImageFormat)))})")

    @classmethod
    def for_extension(cls, extension: str) -> Optional["ImageFormat"]:
        """
        Gets the image format for the given extension.

        :param extension:   The extension.
        :return:            The image format.
        """
        # Remove a leading dot if applicable
        if extension.startswith("."):
            extension = extension[1:]

        for image_format in ImageFormat:
            if extension in image_format.value:
                return image_format

        return None

    def get_default_extension(self) -> str:
        """
        Gets the default extension for the image format.
        """
        return self.name.lower()

    def __str__(self) -> str:
        return self.get_default_extension()

    def cli_repr(self) -> str:
        return self.get_default_extension()

    @classmethod
    def from_cli_repr(cls, cli_string: str) -> 'ImageFormat':
        image_format = cls.for_extension(cli_string)

        if image_format is None:
            raise ValueError(f"Unrecognised image format '{cli_string}'")

        return image_format
