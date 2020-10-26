"""
Module defining the ROI external format.
"""
from typing import Tuple, List

from ....domain.image import Image
from ._ROIObject import ROIObject


# Image info, ROI annotations
ROIExternalFormat = Tuple[Image, List[ROIObject]]
