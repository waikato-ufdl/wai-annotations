"""
Module defining the VGG external format.
"""
from typing import Tuple

from ...vgg_utils.configuration import Image
from .._ImageInfo import ImageInfo

# Image data, VGG Image JSON format
VGGExternalFormat = Tuple[ImageInfo, Image]
