"""
Module defining the COCO external format.
"""
from typing import Tuple, List

from ...coco_utils.configuration import Annotation
from .._ImageInfo import ImageInfo

# Image info, COCO annotations, labels, prefixes
COCOExternalFormat = Tuple[ImageInfo, List[Annotation], List[str], List[str]]
