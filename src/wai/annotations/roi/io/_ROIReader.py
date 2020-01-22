import os
import re
from typing import Iterator
import csv

from ...core import Reader, ImageInfo
from ...core.utils import extension_to_regex, get_associated_image
from .. import constants
from .._format import ROIExternalFormat
from .._ROIObject import ROIObject


class ROIReader(Reader[ROIExternalFormat]):
    """
    Reader of ROI-format CSV files.
    """
    def read_annotation_file(self, filename: str) -> Iterator[ROIExternalFormat]:
        # Read in the file
        with open(filename, "r") as file:
            # Create a CSV dict reader around the file
            csv_reader = csv.DictReader(file)

            # Extract the contents into dictionaries
            roi_dicts = [dict(row) for row in csv_reader]

        # Get the image filename
        if len(roi_dicts) > 0:
            image_file = roi_dicts[0]["file"]
        else:
            matcher = re.compile(extension_to_regex(constants.DEFAULT_EXTENSION))

            image_file = get_associated_image(matcher.match(filename).group(1))

            # Make sure an associated image was found
            if image_file is None:
                raise ValueError(f"No associated image found for {filename}")
            
            image_file = os.path.basename(image_file)

        # Get the full path to the image
        image_path = os.path.join(os.path.dirname(filename), image_file)

        # Create the ROI objects from the dictionaries
        roi_objects = list(map(ROIObject.from_dict, roi_dicts))

        yield ImageInfo.from_file(image_path), roi_objects

    def image_info_to_external_format(self, image_info: ImageInfo) -> ROIExternalFormat:
        return image_info, []
