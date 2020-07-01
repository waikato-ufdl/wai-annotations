"""
Package for built-in ISP specifiers, so they can be loaded without loading
the dependencies of the ISPs.
"""
from ._BoxBoundsCoercionISPSpecifier import BoxBoundsCoercionISPSpecifier
from ._MaskBoundsCoercionISPSpecifier import MaskBoundsCoercionISPSpecifier

from ._DimensionDiscarderISPSpecifier import DimensionDiscarderISPSpecifier

from ._DuplicateFileNamesISPSpecifier import DuplicateFileNamesISPSpecifier

from ._PassThroughISPSpecifier import PassThroughISPSpecifier
