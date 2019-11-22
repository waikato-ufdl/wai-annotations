"""
Module defining the VGG external format.
"""
from typing import Tuple

from ...vgg_utils.configuration import Image
from .._ImageFormat import ImageFormat

# Image data, image format, VGG Image JSON format
VGGExternalFormat = Tuple[bytes, ImageFormat, Image]
