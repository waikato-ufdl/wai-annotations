import os
import re
from typing import Optional, Tuple, List

from ....domain.image import ImageFormat
from ....domain.image.util import get_associated_image
from ..constants import DEFAULT_EXTENSION


def roi_filename_for_image(image_filename: str,
                           prefix: Optional[str] = None,
                           suffix: Optional[str] = None) -> str:
    """
    Creates a filename for the ROI CSV file from the given image filename.

    :param image_filename:  The image filename.
    :param prefix:          The optional prefix to the filename.
    :param suffix:          The optional suffix to the filename.
    :return:                The ROI CSV filename.
    """
    # Set defaults for prefix and suffix
    prefix, suffix = handle_fix_defaults(prefix, suffix)

    return f"{prefix}{os.path.splitext(image_filename)[0]}{suffix}"


def get_associated_image_from_filename(roi_filename: str,
                                       prefix: Optional[str] = None,
                                       suffix: Optional[str] = None,
                                       preference_order: Optional[List[ImageFormat]] = None) -> str:
    """
    Gets the associated image filename for a given ROI filename.

    :param roi_filename:        The filename of the ROI file.
    :param prefix:              The prefix for the ROI filename.
    :param suffix:              The suffix for the ROI filename.
    :param preference_order:    The preferred format order in which to search for images.
    :return:                    The image filename.
    """
    # Get the necessary fix defaults
    prefix, suffix = handle_fix_defaults(prefix, suffix)

    # Create a regex matcher to extract the image basename from the ROI filename
    matcher = re.compile(f"(.*){prefix}(.*){suffix}$")

    # Match the ROI filename
    match = matcher.match(roi_filename)

    # Create the base image filename
    image_file = match.group(1) + match.group(2)

    # Find the image file that matches this name
    image_file = get_associated_image(image_file, preference_order)

    # Make sure an associated image was found
    if image_file is None:
        raise ValueError(f"No associated image found for {roi_filename}")

    return os.path.basename(image_file)


def handle_fix_defaults(prefix: Optional[str] = None,
                        suffix: Optional[str] = None) -> Tuple[str, str]:
    """
    Returns the prefix and suffix values, using defaults where
    values aren't supplied.

    :param prefix:  The prefix, or None to get the default.
    :param suffix:  The suffix, or None to get the default.
    :return:        The prefix and suffix to use.
    """
    # Get the defaults where necessary
    prefix = prefix if prefix is not None else ""
    suffix = suffix if suffix is not None else DEFAULT_EXTENSION

    return prefix, suffix
