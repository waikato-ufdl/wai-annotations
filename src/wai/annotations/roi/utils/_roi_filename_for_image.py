import os
from typing import Optional

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
    prefix = prefix if prefix is not None else ""
    suffix = suffix if suffix is not None else DEFAULT_EXTENSION

    return f"{prefix}{os.path.splitext(image_filename)[0]}{suffix}"
