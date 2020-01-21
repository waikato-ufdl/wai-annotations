from wai.common.adams.imaging.locateobjects import LocatedObject
from wai.common.adams.imaging.locateobjects.constants import KEY_POLY_X, KEY_POLY_Y

from ._Coercion import Coercion


class BoxBoundsCoercion(Coercion):
    """
    Coerces the bounds of the annotations to all be bounding boxes.
    Annotations which have polygon bounds have their bounding box
    set to the minimally-fitted box around the polygon, and the polygon
    itself is removed.
    """
    def _process_located_object(self, located_object: LocatedObject):
        if KEY_POLY_X in located_object.metadata:
            del located_object.metadata[KEY_POLY_X]
        if KEY_POLY_Y in located_object.metadata:
            del located_object.metadata[KEY_POLY_Y]
