from wai.common.adams.imaging.locateobjects import LocatedObject
from wai.common.geometry import Polygon, Point

from ._Coercion import Coercion


class MaskBoundsCoercion(Coercion):
    """
    Coerces the bounds of the annotations to all be polygon-masks.
    Annotations which already have polygons keep theirs, but those
    without are given a rectangular polygon in the shape of their
    bounding box.
    """
    def _process_located_object(self, located_object: LocatedObject):
        # Do nothing if the object already has a polygon
        if located_object.has_polygon():
            return

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
