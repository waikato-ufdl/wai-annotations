import numpy as np

from wai.common.geometry import Rectangle


def mask_from_rectangle(
        rectangle: Rectangle,
        image_width: int,
        image_height: int
) -> np.ndarray:
    """
    Creates a mask from an object's rectangle.

    :param rectangle:       The object's bounding rectangle.
    :param image_width:     The width of the image.
    :param image_height:    The height of the image.
    :return:                An array covering the image, 1 inside the polygon and 0 outside.
    """
    indices = np.indices((image_height, image_width))

    in_rect = np.logical_and(indices[1] <= rectangle.right(), indices[1] >= rectangle.left())
    in_rect = np.logical_and(in_rect, indices[0] >= rectangle.top())
    in_rect = np.logical_and(in_rect, indices[0] <= rectangle.bottom())

    return in_rect
