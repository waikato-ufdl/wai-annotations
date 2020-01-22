import os
from typing import Iterable

from wai.common.file.report import save

from ...core import SeparateImageWriter, ImageInfo
from .._format import ADAMSExternalFormat
from .. import constants


class ADAMSReportWriter(SeparateImageWriter[ADAMSExternalFormat]):
    def write_without_images(self, instances: Iterable[ADAMSExternalFormat], path: str):
        # Path must be a directory
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory, or does not exist")

        # Write each instance
        for instance in instances:
            # Unpack the instance
            image_info, report = instance

            # Format the report filename
            report_filename = f"{os.path.splitext(image_info.filename)[0]}{constants.DEFAULT_EXTENSION}"

            # Save the report
            save(report, os.path.join(path, report_filename))

    def extract_image_info_from_external_format(self, instance: ADAMSExternalFormat) -> ImageInfo:
        # Unpack the instance
        image_info, report = instance

        return image_info
