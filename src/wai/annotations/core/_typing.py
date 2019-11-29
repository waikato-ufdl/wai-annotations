"""
Module for types associated with core functionality.
"""
from typing import Tuple

from wai.common.adams.imaging.locateobjects import LocatedObjects

from ._ImageInfo import ImageInfo

# The internal type used as an intermediary for conversions
# Image info and objects located in image
InternalFormat = Tuple[ImageInfo, LocatedObjects]
