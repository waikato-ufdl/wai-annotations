import os
import csv

from wai.common.cli.options import TypedOption

from ....core.component.util import AnnotationFileProcessor
from ....core.stream import ThenFunction
from ....domain.image import Image, ImageFormat
from ..util import ROIExternalFormat, ROIObject, get_associated_image_from_filename, consume_comments


class ROIReader(AnnotationFileProcessor[ROIExternalFormat]):
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

    reader_prefix = TypedOption(
        "--prefix",
        type=str,
        help="the prefix for output filenames (default = '')"
    )

    reader_suffix = TypedOption(
        "--suffix",
        type=str,
        help="the suffix for output filenames (default = '-rois.csv')"
    )

    def read_annotation_file(self, filename: str, then: ThenFunction[ROIExternalFormat]):
        # Read in the file
        with open(filename, "r") as file:
            # Consume the comments lines
            consume_comments(file)

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

        then((Image.from_file(image_path), roi_objects))

    def read_negative_file(self, filename: str, then: ThenFunction[ROIExternalFormat]):
        then((Image.from_file(filename), []))
