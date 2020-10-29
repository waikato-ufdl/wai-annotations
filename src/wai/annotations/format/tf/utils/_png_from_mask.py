from io import BytesIO

import numpy as np

import PIL


def png_from_mask(mask: np.ndarray) -> bytes:
    """
    Encodes a binary image mask as a PNG file.

    :param mask:    The image mask to encode.
    :return:        The PNG file data.
    """
    # Write the bitmask into PNG format
    output_io = BytesIO()
    image = PIL.Image.fromarray(mask)
    image.save(output_io, format="PNG")

    return output_io.getvalue()
