"""
Package for coercions. Coercions are stream processors which work on
the internal format of the annotations before they are converted
to an external format, moulding the information in the annotations
in a pre-specified manner.
"""
from ._BoxBoundsCoercion import BoxBoundsCoercion
from ._Coercion import Coercion
from ._MaskBoundsCoercion import MaskBoundsCoercion
