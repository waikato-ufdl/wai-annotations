"""
Module defining the ADAMS report-style external format.
"""
from typing import Tuple, Optional

from wai.common.file.report import Report

from ....domain.image import Image

# Image info, report containing located objects
ADAMSExternalFormat = Tuple[Image, Optional[Report]]
