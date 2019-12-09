import os
from enum import Enum
from typing import Optional
from itertools import chain


class ImageFormat(Enum):
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
    def get_associated_image(cls, filename: str) -> Optional[str]:
        """
        Gets an image associated with the given filename, by searching for
        a file with one of the valid image format extensions.

        :param filename:    The filename to find an image for, without extension.
        :return:            The filename of the image, None if not found.
        """
        # Check each variation of the extension for each format
        for image_format in ImageFormat:
            for extension in image_format.value:
                # Get the hypothetical filename for an image of this format
                image_filename: str = f"{filename}.{extension}"

                # If an image of this format exists, return it
                if os.path.exists(image_filename):
                    return image_filename

        # No image found
        return None

    @classmethod
    def for_extension(cls, extension: str) -> Optional["ImageFormat"]:
        """
        Gets the image format for the given extension.

        :param extension:   The extension.
        :return:            The image format.
        """
        for image_format in ImageFormat:
            if extension in image_format.value:
                return image_format

        return None

    def get_default_extension(self) -> str:
        """
        Gets the default extension for the image format.
        """
        return self.name.lower()
