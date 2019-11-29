"""
Module for implementing the coercion of located objects into
either bounding-box format or polygon mask format.
"""
from wai.common.adams.imaging.locateobjects.constants import KEY_POLY_X, KEY_POLY_Y
from wai.common.geometry import Polygon, Point

from ..core import InternalFormat


def coerce_bbox(instance: InternalFormat) -> InternalFormat:
    """
    Coerces an instance to use bounding-box format object bounds.

    :param instance:    The instance to coerce.
    :return:            The same instance after coercion.
    """
    # Get the located objects from the instance
    image_info, located_objects = instance

    # Process each located object
    for located_object in located_objects:
        if KEY_POLY_X in located_object.metadata:
            del located_object.metadata[KEY_POLY_X]
        if KEY_POLY_Y in located_object.metadata:
            del located_object.metadata[KEY_POLY_Y]

    return instance


def coerce_mask(instance: InternalFormat) -> InternalFormat:
    """
    Coerces an instance to use polygon-mask format object bounds.

    :param instance:    The instance to coerce.
    :return:            The same instance after coercion.
    """
    # Get the located objects from the instance
    image_info, located_objects = instance

    # Process each located object
    for located_object in located_objects:
        # Do nothing if the object already has a polygon
        if located_object.has_polygon():
            continue

        # Calculate the bound coordinates
        rectangle = located_object.get_rectangle()
        left = rectangle.left()
        right = rectangle.right()
        top = rectangle.top()
        bottom = rectangle.bottom()

        # Create a polygon from the bound coordinates
        polygon = Polygon(Point(left, top),
                          Point(right, top),
                          Point(right, bottom),
                          Point(left, bottom))

        # Add the polygon to the object
        located_object.set_polygon(polygon)

    return instance
