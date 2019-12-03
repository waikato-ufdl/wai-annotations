import os
from typing import Iterable, Tuple
import csv

from ...core import SeparateImageWriter, ImageInfo
from ...core.external_formats import ROIExternalFormat, ROIObject


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

            # Write the CSV file
            with open(os.path.join(path, filename), "w") as file:
                csv_writer = csv.DictWriter(file, self.header())
                csv_writer.writeheader()
                for roi_object in roi_objects:
                    row = roi_object.as_dict()
                    row.update(file=image_info.filename)
                    csv_writer.writerow(row)

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

    def header(self) -> Tuple[str, ...]:
        """
        Gets the ROI header.

        :return:    The header.
        """
        return ("file", *ROIObject.keywords())
