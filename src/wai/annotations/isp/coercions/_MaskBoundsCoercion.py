from wai.common.adams.imaging.locateobjects import LocatedObject

from ...domain.image.object_detection.util import polygon_from_rectangle
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

        # Add the polygon to the object
        located_object.set_polygon(polygon_from_rectangle(located_object.get_rectangle()))
