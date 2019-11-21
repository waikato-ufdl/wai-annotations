"""
Module defining the ADAMS report-style external format.
"""
from typing import Tuple

from wai.common.file.report import Report

from .._ImageFormat import ImageFormat

# Image filename, image data, image format, report containing located objects
ADAMSExternalFormat = Tuple[str, bytes, ImageFormat, Report]
