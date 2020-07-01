"""
Module defining the VGG external format.
"""
from typing import Tuple

from ...domain.image import ImageInfo
from .configuration import Image

# Image data, VGG Image JSON format
VGGExternalFormat = Tuple[ImageInfo, Image]
