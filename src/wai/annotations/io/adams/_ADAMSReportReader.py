import os
from typing import Iterator

from wai.common.file.report import loadf, Report

from ...core import PerImageReader, ImageFormat, ImageInfo
from ...core.external_formats import ADAMSExternalFormat


class ADAMSReportReader(PerImageReader[ADAMSExternalFormat]):
    """
    Reader of ADAMS .report files.
    """
    @classmethod
    def input_help_text(cls) -> str:
        return "input directory with report files or text file with one absolute report file name per line"

    @classmethod
    def get_default_file_regex(cls) -> str:
        return ".*\\.report"

    def read(self, filename: str) -> Iterator[ADAMSExternalFormat]:
        # Get the image associated to this report
        image_file = ImageFormat.get_associated_image(filename)

        # Load the image
        image_data = None
        if image_file is not None:
            with open(image_file, "rb") as file:
                image_data = file.read()

        # Strip the image file down to just it's base name
        image_file = os.path.basename(image_file)

        # Create the image info object
        image_info = ImageInfo(image_file, image_data)

        # Load the report
        report: Report = loadf(filename)

        yield image_info, report
