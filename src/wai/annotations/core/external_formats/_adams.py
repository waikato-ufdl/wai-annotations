"""
Module defining the ADAMS report-style external format.
"""
from typing import Tuple

from wai.common.file.report import Report

from .._ImageInfo import ImageInfo

# Image info, report containing located objects
ADAMSExternalFormat = Tuple[ImageInfo, Report]
