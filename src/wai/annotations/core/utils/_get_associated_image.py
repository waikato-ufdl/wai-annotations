import os
from typing import Optional


def get_associated_image(filename: str) -> Optional[str]:
    """
    Gets an image associated with the given filename. Searches for
    a file with the given filename and a valid image format extension.

    :param filename:    The filename to find an image for, without extension.
    :return:            The filename of the found image, None if not found.
    """
    # Check each variation of the extension for each format
    from .._Settings import get_settings
    for image_format in get_settings().IMAGE_FORMAT_PREFERENCE_ORDER:
        for extension in image_format.value:
            # Get the hypothetical filename for an image of this format
            image_filename: str = f"{filename}.{extension}"

            # If an image of this format exists, return it
            if os.path.exists(image_filename):
                return image_filename

    # No image found
    return None
