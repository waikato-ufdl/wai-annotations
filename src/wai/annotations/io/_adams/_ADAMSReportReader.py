import os
from typing import Iterator, Iterable

from wai.common.file.report import loadf, Report

from ...core import Reader, ImageFormat, ImageInfo
from ...core.external_formats import ADAMSExternalFormat
from ...core.utils import get_files_from_directory
from .constants import EXTENSION


class ADAMSReportReader(Reader[ADAMSExternalFormat]):
    """
    Reader of ADAMS .report files.
    """
    def determine_input_files(self, input_path: str) -> Iterable[str]:
        # If given a directory as input, recursively load all
        # report files in the directory
        if os.path.isdir(input_path):
            return get_files_from_directory(input_path, EXTENSION)

        # Otherwise we expect a file containing a list of reports
        else:
            with open(input_path, "r") as file:
                return (line.strip() for line in file)

    @classmethod
    def input_help_text(cls) -> str:
        return "input directory with report files or text file with one absolute report file name per line"

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
