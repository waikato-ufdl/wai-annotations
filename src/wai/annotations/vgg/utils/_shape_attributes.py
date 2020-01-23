from typing import Tuple, Union

from wai.common.adams.imaging.locateobjects import LocatedObject
from wai.common.geometry import Polygon, Point

from ..configuration import PolygonShapeAttributes, RectShapeAttributes


def from_polygon_shape_attributes(shape_attributes: PolygonShapeAttributes) -> Tuple[int, int, int, int, Polygon]:
    """
    Gets the bounds and the polygon for a located object from
    the polygon shape attributes of a region.

    :param shape_attributes:    The shape attributes.
    :return:                    The x, y, width, height and polygon of the located object.
    """
    # Get the polygon
    polygon = Polygon(*(Point(x, y) for x, y in zip(shape_attributes.all_points_x, shape_attributes.all_points_y)))

    # Get the top/left coordinates
    x = min(shape_attributes.all_points_x)
    y = min(shape_attributes.all_points_y)

    # Get the width and height
    width = max(shape_attributes.all_points_x) - x + 1
    height = max(shape_attributes.all_points_y) - y + 1

    return x, y, width, height, polygon


def from_rect_shape_attributes(shape_attributes: RectShapeAttributes) -> Tuple[int, int, int, int]:
    """
    Gets the bounds for a located object from the
    rectangular shape attributes of a region.

    :param shape_attributes:    The shape attributes.
    :return:                    The x, y, width and height of the located object.
    """
    return shape_attributes.x, shape_attributes.y, shape_attributes.width, shape_attributes.height


def get_shape_attributes(located_object: LocatedObject) -> Union[RectShapeAttributes, PolygonShapeAttributes]:
    """
    Gets the shape attributes of the given located object.
    The type of the attributes is determined by whether
    the object is in bbox or mask format.

    :param located_object:  The located object.
    :return:                The shape attributes.
    """
    # Mask format
    if located_object.has_polygon():
        return PolygonShapeAttributes(name="polygon",
                                      all_points_x=located_object.get_polygon_x(),
                                      all_points_y=located_object.get_polygon_y())
    # Bbox format
    else:
        return RectShapeAttributes(name="rect",
                                   x=located_object.x,
                                   y=located_object.y,
                                   width=located_object.width,
                                   height=located_object.height)
