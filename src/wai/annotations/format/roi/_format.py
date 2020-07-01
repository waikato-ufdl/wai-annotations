"""
Module defining the ROI external format.
"""
from typing import Tuple, List

from ...domain.image import ImageInfo
from ._ROIObject import ROIObject


# Image info, ROI annotations
ROIExternalFormat = Tuple[ImageInfo, List[ROIObject]]
