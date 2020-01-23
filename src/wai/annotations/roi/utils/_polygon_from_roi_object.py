from wai.common.geometry import Polygon, Point

from .._ROIObject import ROIObject


def polygon_from_roi_object(roi_object: ROIObject) -> Polygon:
    """
    Generates a polygon from the given ROI object.

    :param roi_object:  The ROI object.
    :return:            The polygon.
    """
    # Make sure the ROI object has a polygon
    if not roi_object.has_polygon():
        raise ValueError(f"ROI object has no polygon")

    return Polygon(*(Point(round(x), round(y))
                     for x, y in zip(roi_object.poly_x, roi_object.poly_y)))
