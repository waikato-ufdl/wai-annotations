"""
Module defining the COCO external format.
"""
from typing import Tuple, List

from ....domain.image import Image
from ..configuration import Annotation

# Image info, COCO annotations, labels, prefixes
COCOExternalFormat = Tuple[Image, List[Annotation], List[str], List[str]]
