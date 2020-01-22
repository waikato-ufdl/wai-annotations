import os
from typing import Iterable, Tuple
import csv

from ...core import SeparateImageWriter, ImageInfo
from ...core.external_formats import ROIExternalFormat
from ...roi_utils import ROIObject, combine_dicts


class ROIWriter(SeparateImageWriter[ROIExternalFormat]):
    """
    Writer of ROI CSV annotations.
    """
    @classmethod
    def output_help_text(cls) -> str:
        return "output directory to write files to"

    def write_without_images(self, instances: Iterable[ROIExternalFormat], path: str):
        # Path must be a directory
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory, or does not exist")

        # Write each instance
        for instance in instances:
            # Unpack the instance
            image_info, roi_objects = instance

            # Format the report filename
            filename: str = self.filename_from_image_filename(image_info.filename)

            # Format each ROI object as a dictionary
            roi_dicts, headers = combine_dicts(map(ROIObject.as_dict, roi_objects))

            # Put the headers in order
            headers = tuple(header for header in ROIObject.keywords
                            if header in headers or header in ROIObject.required_keyword_set)

            # Add the filename header
            headers = "file", *headers

            # Write the CSV file
            with open(os.path.join(path, filename), "w") as file:
                csv_writer = csv.DictWriter(file, headers)
                csv_writer.writeheader()
                for roi_dict in roi_dicts:
                    roi_dict.update(file=image_info.filename)
                    csv_writer.writerow(roi_dict)

    def extract_image_info_from_external_format(self, instance: ROIExternalFormat) -> ImageInfo:
        # Unpack the instance
        image_info, roi_objects = instance

        return image_info

    def filename_from_image_filename(self, image_filename: str) -> str:
        """
        Creates a filename for the ROI CSV file from the given image filename.

        :param image_filename:  The image filename.
        :return:                The ROI CSV filename.
        """
        return f"{os.path.splitext(image_filename)[0]}-roi.csv"
