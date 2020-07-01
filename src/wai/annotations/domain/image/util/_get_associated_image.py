import os
from typing import Optional, List

from .._ImageFormat import ImageFormat


def get_associated_image(filename: str,
                         preference_order: Optional[List[ImageFormat]] = None) -> Optional[str]:
    """
    Gets an image associated with the given filename. Searches for
    a file with the given filename and a valid image format extension.

    :param filename:            The filename to find an image for, without extension.
    :param preference_order:    The preferred format order in which to search for images.
    :return:                    The filename of the found image, None if not found.
    """
    # Use any preference order if none is supplied
    if preference_order is None:
        preference_order = list(ImageFormat)

    # Check each variation of the extension for each format
    for image_format in preference_order:
        for extension in image_format.possible_extensions:
            # Get the hypothetical filename for an image of this format
            image_filename: str = f"{filename}.{extension}"

            # If an image of this format exists, return it
            if os.path.exists(image_filename):
                return image_filename

    # No image found
    return None
