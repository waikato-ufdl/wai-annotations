import io
from typing import Tuple

from PIL import Image


def get_image_size(image_data: bytes) -> Tuple[int, int]:
    """
    Gets the size of the image from the data.

    :param image_data:  The image data.
    :return:            The width and height of the image.
    """
    image = Image.open(io.BytesIO(image_data))

    return image.width, image.height
