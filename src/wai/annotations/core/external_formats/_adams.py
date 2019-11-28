"""
Module defining the ADAMS report-style external format.
"""
from typing import Tuple, Optional

from wai.common.file.report import Report

# Image filename, image data, report containing located objects
ADAMSExternalFormat = Tuple[str, Optional[bytes], Report]
