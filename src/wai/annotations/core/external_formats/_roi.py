"""
Module defining the ROI external format.
"""
from typing import Tuple, List

from ...roi_utils import ROIObject
from .._ImageInfo import ImageInfo


# Image info, ROI annotations
ROIExternalFormat = Tuple[ImageInfo, List[ROIObject]]
