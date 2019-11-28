"""
Module defining the COCO external format.
"""
from typing import Tuple, List, Optional

from ...coco_utils.configuration import Annotation

# Image filename, image data, COCO annotations, labels, prefixes
COCOExternalFormat = Tuple[str, Optional[bytes], List[Annotation], List[str], List[str]]
