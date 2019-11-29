import os
from typing import Iterator, Iterable
import csv

from ...core import Reader, ImageInfo
from ...core.external_formats import ROIExternalFormat, ROIObject
from ...core.utils import get_files_from_directory
from .constants import EXTENSION


class ROIReader(Reader[ROIExternalFormat]):
    """
    Reader of ROI-format CSV files.
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
        return "input directory with ROI csv files or text file with one absolute ROI file name per line"

    def read(self, filename: str) -> Iterator[ROIExternalFormat]:
        # Read in the file
        with open(filename, "r") as file:
            # Create a CSV dict reader around the file
            csv_reader = csv.DictReader(file)

            # Extract the contents into dictionaries
            roi_dicts = [dict(row) for row in csv_reader]

        # Get the image filename
        image_file = roi_dicts[0]["file"]

        # Get the full path to the image
        image_path = os.path.join(os.path.dirname(filename), image_file)

        # Load the image
        image_data = None
        if os.path.exists(image_path):
            with open(image_path, "rb") as file:
                image_data = file.read()

        # Create the ROI objects from the dictionaries
        roi_objects = list(map(ROIObject.from_dict, roi_dicts))

        yield ImageInfo(image_file, image_data), roi_objects
