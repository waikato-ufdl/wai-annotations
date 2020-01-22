import io

import numpy as np
from skimage import measure
import PIL
from wai.common.geometry import Polygon, Point


def polygon_from_mask(mask: bytes) -> Polygon:
    """
    Converts the PNG format mask into a polygon.

    :param mask:    The PNG mask.
    :return:        A polygon.
    """
    # Decode the PNG
    image = PIL.Image.open(io.BytesIO(mask))

    # Convert to a bitmask
    binary_mask = np.asarray(image)

    # Use find_contours to find the (only) polygon in the bit-mask
    poly_array = measure.find_contours(binary_mask, 0.9, "high")[0]

    # Convert to a Polygon
    polygon = Polygon()
    for p in range(poly_array.shape[0]):
        polygon.points.append(Point(int(round(poly_array[p, 1])), int(round(poly_array[p, 0]))))

    # Remove redundant line segments
    polygon.simplify()

    return polygon
