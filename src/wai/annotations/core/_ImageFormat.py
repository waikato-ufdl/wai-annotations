import os
from enum import Enum
from typing import Tuple, Optional


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
        for image_format in ImageFormat:
            if extension in image_format.value:
                return image_format

        return None

    @classmethod
    def get_associated_image(cls, filename: str) -> Optional[str]:
        """
        Gets an image associated with the given filename, by replacing its
        extension with one of the valid image formats.

        :param filename:    The filename to find an image for.
        :return:            The filename of the image, None if not found.
        """
        # Remove the extension from the filename
        filename = os.path.splitext(filename)[0]

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
