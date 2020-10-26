import numpy as np

from wai.common.geometry import Polygon


def polygon_to_poly_array(polygon: Polygon) -> np.ndarray:
    """
    Converts a polygon into an interleaved array as expected by
    image_utils.polygon_to_mask.

    :param polygon:     The polygon.
    :return:            The array.
    """
    # Flatten the polygon points into a list
    poly_list = []
    for point in polygon:
        poly_list.append(point.x)
        poly_list.append(point.y)

    # Create a Numpy array for the polygon
    return np.array(poly_list, dtype=float)
