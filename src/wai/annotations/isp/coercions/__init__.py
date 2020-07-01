"""
Package for coercions. Coercions are inline stream processors which work on
object detection bounds, converting box-bounds to polygons or vice-versa.
"""
from ._BoxBoundsCoercion import BoxBoundsCoercion
from ._Coercion import Coercion
from ._MaskBoundsCoercion import MaskBoundsCoercion
