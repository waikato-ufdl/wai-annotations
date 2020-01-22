import os
from typing import Iterator

from wai.common.file.report import loadf, Report

from ...core import Reader, ImageInfo
from ...core.utils import get_associated_image
from .._format import ADAMSExternalFormat


class ADAMSReportReader(Reader[ADAMSExternalFormat]):
    """
    Reader of ADAMS .report files.
    """
    def read_annotation_file(self, filename: str) -> Iterator[ADAMSExternalFormat]:
        # Get the image associated to this report
        image_file = get_associated_image(os.path.splitext(filename)[0])

        # Make sure an image file was found
        if image_file is None:
            raise ValueError(f"No associated image found for {filename}")

        # Create the image info object
        image_info = ImageInfo.from_file(image_file)

        # Load the report
        report: Report = loadf(filename)

        yield image_info, report

    def image_info_to_external_format(self, image_info: ImageInfo) -> ADAMSExternalFormat:
        return image_info, Report()
