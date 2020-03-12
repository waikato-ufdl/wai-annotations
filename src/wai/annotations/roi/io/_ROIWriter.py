import os
from typing import Iterable, IO
import csv

from wai.common.cli.options import TypedOption

from ...core import SeparateImageWriter, ImageInfo
from ..utils import combine_dicts, roi_filename_for_image
from ..constants import COMMENT_SYMBOL
from .._format import ROIExternalFormat
from .._ROIObject import ROIObject


class ROIWriter(SeparateImageWriter[ROIExternalFormat]):
    """
    Writer of ROI CSV annotations.
    """
    writer_prefix = TypedOption(
        "--prefix",
        type=str,
        help="the prefix for output filenames (default = '')"
    )

    writer_suffix = TypedOption(
        "--suffix",
        type=str,
        help="the suffix for output filenames (default = '-rois.csv')"
    )

    comments = TypedOption(
        "--comments",
        type=str,
        nargs="+",
        help="comments to write to the beginning of the ROI file"
    )

    def write_without_images(self, instances: Iterable[ROIExternalFormat], path: str):
        # Path must be a directory
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory, or does not exist")

        # Write each instance
        for instance in instances:
            # Unpack the instance
            image_info, roi_objects = instance

            # Format the report filename
            filename: str = roi_filename_for_image(image_info.filename, self.writer_prefix, self.writer_suffix)

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
                self._write_comments(file)
                csv_writer = csv.DictWriter(file, headers)
                csv_writer.writeheader()
                for roi_dict in roi_dicts:
                    roi_dict.update(file=image_info.filename)
                    csv_writer.writerow(roi_dict)

    def extract_image_info_from_external_format(self, instance: ROIExternalFormat) -> ImageInfo:
        # Unpack the instance
        image_info, roi_objects = instance

        return image_info

    def expects_file(self) -> bool:
        return False

    @classmethod
    def output_help_text(cls) -> str:
        return "output directory to write files to"

    def _write_comments(self, file: IO[str]):
        """
        Writes the supplied comments to the given file.

        :param file:    The file to write to.
        """
        # Write each entry on its own line
        for comment_line in self.comments:
            # Add the comment symbol if it's not there already
            if not comment_line.startswith(COMMENT_SYMBOL):
                comment_line = f"{COMMENT_SYMBOL} {comment_line}"

            # Write the comment
            file.write(f"{comment_line}\n")
