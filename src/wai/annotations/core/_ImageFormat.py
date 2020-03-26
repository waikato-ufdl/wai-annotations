import os
from enum import Enum
from typing import Optional, FrozenSet
from itertools import chain

from wai.common.cli import CLIRepresentable


class ImageFormat(CLIRepresentable, Enum):
    """
    Class enumerating the types of images we can work with. Each enumeration's
    value is the set of possible file extensions for that image type, followed
    by its PIL format string.
    """
    JPG = frozenset({"jpg", "JPG", "jpeg", "JPEG"}), "JPEG"
    PNG = frozenset({"png", "PNG"}), "PNG"
    BMP = frozenset({"bmp", "BMP"}), "BMP"

    @property
    def possible_extensions(self) -> FrozenSet[str]:
        """
        Gets the set of possible extensions for this format.
        """
        return self.value[0]

    @property
    def pil_format_string(self) -> str:
        """
        Gets the PIL format string for this format.
        """
        return self.value[1]

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
                         f"({', '.join(chain(*(image_format.possible_extensions for image_format in ImageFormat)))})")

    def replace_extension(self, filename: str) -> str:
        """
        Replaces the extension of an image filename with the
        default extension for this format.

        :param filename:    The filename to modify.
        :return:            The new filename.
        """
        # Get the extension from the filename
        extension: str = os.path.splitext(filename)[1][1:]

        # Remove the extension from the filename
        filename = filename[:-len(extension)]

        # Choose a new extension for the filename
        extension = self.get_default_extension().upper() if extension.isupper() else self.get_default_extension()

        return filename + extension

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

        # Lowercase the extension
        extension = extension.lower()

        # Try find a format for the extension
        for image_format in ImageFormat:
            if extension in image_format.possible_extensions:
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
        # The CLI representation is any known extension
        image_format = cls.for_extension(cli_string)

        # If the extension is unknown, raise an issue
        if image_format is None:
            raise ValueError(f"Unrecognised image format '{cli_string}'")

        return image_format
