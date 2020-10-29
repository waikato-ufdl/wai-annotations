import os
from typing import IO
import csv

from wai.common.cli.options import TypedOption, FlagOption

from ....core.component.util import (
    SplitSink,
    SeparateFileWriter,
    RequiresNoSplitFinalisation,
    ExpectsDirectory
)
from ..constants import COMMENT_SYMBOL
from ..util import combine_dicts, roi_filename_for_image, ROIExternalFormat, ROIObject


class ROIWriter(
    ExpectsDirectory,
    RequiresNoSplitFinalisation,
    SplitSink[ROIExternalFormat], SeparateFileWriter[ROIExternalFormat]
):
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

    size_mode = FlagOption(
        "--size-mode",
        help="writes the ROI files with x,y,w,h headers instead of x0,y0,x1,y1"
    )

    def start(self):
        super().start()

        # Path must be a directory
        if not os.path.isdir(self.output):
            raise ValueError(f"{self.output} is not a directory, or does not exist")

    def consume_element_for_split(
            self,
            element: ROIExternalFormat
    ):
        # Unpack the instance
        image_info, roi_objects = element

        # Format the report filename
        filename: str = roi_filename_for_image(image_info.filename, self.writer_prefix, self.writer_suffix)

        # Format the filename for the ROI file
        roi_filename = self.get_split_path(self.split_label, os.path.join(self.output, filename), True)

        # Write the image
        self.write_data_file(image_info, os.path.dirname(roi_filename))

        # If this is a negative example, we're done
        if len(roi_objects) == 0:
            return

        # Format each ROI object as a dictionary
        roi_dicts, headers = combine_dicts(roi_object.as_dict(self.size_mode) for roi_object in roi_objects)

        # Get the header keywords we are expecting
        keywords = ROIObject.keywords(self.size_mode)

        # Extract the non-standard headers
        non_standard_headers = headers - set(keywords)

        # Put the standard headers in order
        headers = tuple(header for header in keywords
                        if header in headers or header in set(ROIObject.required_keywords(self.size_mode)))

        # Add the filename header
        headers = "file", *headers, *non_standard_headers

        # Write the CSV file
        with open(roi_filename, "w") as file:
            self._write_comments(file)
            csv_writer = csv.DictWriter(file, headers)
            csv_writer.writeheader()
            for roi_dict in roi_dicts:
                roi_dict.update(file=image_info.filename)
                csv_writer.writerow(roi_dict)

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
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
