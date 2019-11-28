"""
Module for types associated with core functionality.
"""
from typing import Tuple, Optional

from wai.common.adams.imaging.locateobjects import LocatedObjects

from ._ImageFormat import ImageFormat

# The internal type used as an intermediary for conversions
# Image filename, optional image data, objects located in image
InternalFormat = Tuple[str, Optional[bytes], LocatedObjects]
