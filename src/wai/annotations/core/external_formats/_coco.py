"""
Module defining the COCO external format.
"""
from typing import Tuple, List

from ...coco_utils.configuration import Annotation
from .._ImageFormat import ImageFormat

# Image filename, image data, image format, COCO annotations, labels
COCOExternalFormat = Tuple[str, bytes, ImageFormat, List[Annotation], List[str]]
