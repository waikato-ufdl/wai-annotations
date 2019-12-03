import os
from typing import Iterator
import csv

from ...core import PerImageReader, ImageInfo
from ...core.external_formats import ROIExternalFormat, ROIObject


class ROIReader(PerImageReader[ROIExternalFormat]):
    """
    Reader of ROI-format CSV files.
    """
    @classmethod
    def input_help_text(cls) -> str:
        return "input directory with ROI csv files or text file with one absolute ROI file name per line"

    @classmethod
    def get_default_file_regex(cls) -> str:
        return ".*-roi\\.csv"

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
