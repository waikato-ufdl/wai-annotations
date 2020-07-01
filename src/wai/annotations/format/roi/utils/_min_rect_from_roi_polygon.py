from typing import List, Tuple

import numpy as np

from ....image_utils import polygon_to_minrect


def min_rect_from_roi_polygon(poly_x: List[float], poly_y: List[float]) -> Tuple[float, float]:
    """
    Gets the width and height of the minimum-area rectangle around
    a ROI object's polygon.

    :param poly_x:  The list of x coordinates of the polygon.
    :param poly_y:  The list of y coordinates of the polygon.
    :return:        The width and height of the minimum-area rectangle.
    """
    # Create the array expected by polygon_to_minrect
    poly_array = np.array(list(zip(poly_x, poly_y)), dtype=np.float32)

    return polygon_to_minrect(poly_array)
