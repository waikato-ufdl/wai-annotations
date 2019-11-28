"""
Module defining the VGG external format.
"""
from typing import Tuple, Optional

from ...vgg_utils.configuration import Image

# Image data, VGG Image JSON format
VGGExternalFormat = Tuple[Optional[bytes], Image]
