import os
from typing import Iterator, IO
import csv

from wai.common.cli.options import TypedOption

from ....core.component import LocalReader
from ....domain.image import ImageInfo, ImageFormat
from ..utils import get_associated_image_from_filename
from ..constants import COMMENT_SYMBOL
from .._format import ROIExternalFormat
from .._ROIObject import ROIObject


class ROIReader(LocalReader[ROIExternalFormat]):
    """
    Reader of ROI-format CSV files.
    """
    # The order of preference of image formats
    image_format_preference_order = TypedOption(
        "-e", "--extensions",
        type=ImageFormat,
        nargs=3,
        metavar="FORMAT",
        default=[ImageFormat.PNG, ImageFormat.JPG, ImageFormat.BMP],
        help="image format extensions in order of preference"
    )

    reader_prefix = TypedOption("--prefix", type=str,
                                help="the prefix for output filenames (default = '')")
    reader_suffix = TypedOption("--suffix", type=str,
                                help="the suffix for output filenames (default = '-rois.csv')")

    def read_annotation_file(self, filename: str) -> Iterator[ROIExternalFormat]:
        # Read in the file
        with open(filename, "r") as file:
            # Consume the comments lines
            self._consume_comments(file)

            # Create a CSV dict reader around the file
            csv_reader = csv.DictReader(file)

            # Extract the contents into dictionaries
            roi_dicts = [dict(row) for row in csv_reader]

        # Get the image filename
        if len(roi_dicts) > 0:
            image_file = roi_dicts[0]["file"]
        else:
            image_file = get_associated_image_from_filename(filename,
                                                            self.reader_prefix,
                                                            self.reader_suffix,
                                                            self.image_format_preference_order)

        # Get the full path to the image
        image_path = os.path.join(os.path.dirname(filename), image_file)

        # Create the ROI objects from the dictionaries
        roi_objects = list(map(ROIObject.from_dict, roi_dicts))

        yield ImageInfo.from_file(image_path), roi_objects

    def read_negative_file(self, filename: str) -> Iterator[ROIExternalFormat]:
        yield ImageInfo.from_file(filename), []

    def _consume_comments(self, file: IO[str]):
        """
        Reads lines from the file until a non-comment line is found.

        :param file:    The file to read from.
        """
        # Read until end of file
        line = None
        while line != '':
            # Record the position in the file so we can backtrack
            # if we find a non-comment line
            position = file.tell()

            # Read the next line from the file
            line = file.readline()

            # If it's not a comment, backtrack and return
            if not line.startswith(COMMENT_SYMBOL):
                file.seek(position)
                return
