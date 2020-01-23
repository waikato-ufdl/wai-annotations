import os
from typing import Iterable
import csv

from ...core import SeparateImageWriter, ImageInfo
from .._combine_dicts import combine_dicts
from .._format import ROIExternalFormat
from .._roi_filename_for_image import roi_filename_for_image
from .._ROIObject import ROIObject


class ROIWriter(SeparateImageWriter[ROIExternalFormat]):
    """
    Writer of ROI CSV annotations.
    """
    def write_without_images(self, instances: Iterable[ROIExternalFormat], path: str):
        # Path must be a directory
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory, or does not exist")

        # Write each instance
        for instance in instances:
            # Unpack the instance
            image_info, roi_objects = instance

            # Format the report filename
            filename: str = roi_filename_for_image(image_info.filename)

            # Format each ROI object as a dictionary
            roi_dicts, headers = combine_dicts(map(ROIObject.as_dict, roi_objects))

            # Extract the non-standard headers
            non_standard_headers = headers - ROIObject.keyword_set

            # Put the standard headers in order
            headers = tuple(header for header in ROIObject.keywords
                            if header in headers or header in ROIObject.required_keyword_set)

            # Add the filename header
            headers = "file", *headers, *non_standard_headers

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
