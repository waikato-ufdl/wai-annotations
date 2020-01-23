from typing import List, Tuple

from wai.common.geometry import Polygon


def roi_polygon(polygon: Polygon) -> Tuple[List[float], List[float]]:
    """
    Converts a polygon into lists of x and y coordinates.

    :param polygon: The polygon.
    :return:        The lists of x and y coordinates.
    """
    # Create the lists
    poly_x, poly_y = [], []

    # Add each point
    for point in polygon:
        poly_x.append(round(point.x))
        poly_y.append(round(point.y))

    return poly_x, poly_y
