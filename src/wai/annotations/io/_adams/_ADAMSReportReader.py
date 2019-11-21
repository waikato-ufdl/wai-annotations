import os
from typing import Iterator, Iterable

from wai.common.file.report import loadf, Report

from ...core import Reader, ImageFormat
from ...core.external_formats import ADAMSExternalFormat
from .constants import EXTENSION


class ADAMSReportReader(Reader[ADAMSExternalFormat]):
    """
    Reader of ADAMS .report files.
    """
    def determine_input_files(self, input_path: str) -> Iterable[str]:
        # If given a directory as input, recursively load all
        # report files in the directory
        if os.path.isdir(input_path):
            return self.get_files_from_directory(input_path)

        # Otherwise we expect a file containing a list of reports
        else:
            with open(input_path, "r") as file:
                return (line.strip() for line in file)

    @classmethod
    def input_help_text(cls) -> str:
        return "input directory with report files or text file with one absolute report file name per line"

    def read(self, filename: str) -> Iterator[ADAMSExternalFormat]:
        # Get the image associated to this report
        image_file, image_format = ImageFormat.get_associated_image(filename)

        # Log a warning if the image wasn't found
        if image_file is None:
            raise RuntimeError(f"Failed to determine image for report: {filename}")

        # Load the image
        with open(image_file, "rb") as file:
            image_data = file.read()

        # Strip the image file down to just it's base name
        image_file = os.path.basename(image_file)

        # Load the report
        report: Report = loadf(filename)

        yield image_file, image_data, image_format, report

    @staticmethod
    def get_files_from_directory(directory: str) -> Iterable[str]:
        """
        Recursively gets the report files from all sub-directories of the
        given directory (including itself).

        :param directory:   The top-level directory to search.
        :return:            The iterator of filenames.
        """
        # Process each subdirectory
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(EXTENSION):
                    yield os.path.join(directory, subdir, file)