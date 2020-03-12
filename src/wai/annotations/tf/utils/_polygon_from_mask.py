import io
from typing import Tuple

import numpy as np
import PIL
from wai.common.geometry import Polygon, Point

from ...image_utils import mask_to_polygon


def polygon_from_mask(mask: bytes,
                      view: Tuple[float, float, float, float],
                      sample_stride: int = 1) -> Polygon:
    """
    Converts the PNG format mask into a polygon.

    :param mask:            The PNG mask.
    :param view:            The area inside the mask to look for the polygon (left, top, right, bottom).
    :param sample_stride:   The stride to step through the mask when finding the polygon. Results
                            in a more coarsely-grained polygon but finishes faster.
    :return:                A polygon.
    """
    # Decode the PNG
    image = PIL.Image.open(io.BytesIO(mask))

    # Convert to a bitmask
    binary_mask = np.asarray(image)

    # Use find_contours to find the (only) polygon in the bit-mask
    poly_array = mask_to_polygon(binary_mask, 0.9,
                                 view=view,
                                 mask_nth=sample_stride,
                                 fully_connected="high")[0]

    # Convert to a Polygon
    polygon = Polygon()
    for p in range(poly_array.shape[0]):
        polygon.points.append(Point(int(round(poly_array[p, 1])), int(round(poly_array[p, 0]))))

    # Remove redundant line segments
    polygon.simplify()

    return polygon
