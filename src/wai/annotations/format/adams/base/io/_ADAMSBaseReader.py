import os
from typing import Iterator

from wai.common.cli.options import TypedOption
from wai.common.file.report import loadf, Report

from .....core.utils import recursive_iglob
from .....core.component import LocalReader
from .....domain.image import ImageInfo, ImageFormat
from .....domain.image.util import get_associated_image
from ...constants import DEFAULT_EXTENSION
from ..._format import ADAMSExternalFormat


class ADAMSBaseReader(LocalReader[ADAMSExternalFormat]):
    """
    Reader of ADAMS .report files.
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

    def read_annotation_file(self, filename: str) -> Iterator[ADAMSExternalFormat]:
        # Get the image associated to this report
        image_file = get_associated_image(os.path.splitext(filename)[0], self.image_format_preference_order)

        # Make sure an image file was found
        if image_file is None:
            raise ValueError(f"No associated image found for {filename}")

        # Create the image info object
        image_info = ImageInfo.from_file(image_file)

        # Load the report
        report: Report = loadf(filename)

        yield image_info, report

    def read_negative_file(self, filename: str) -> Iterator[ADAMSExternalFormat]:
        yield ImageInfo.from_file(filename), Report()

    def get_annotation_files(self) -> Iterator[str]:
        # Further process the set of annotation files
        for file in super().get_annotation_files():
            # If the file is a directory, default to all files that end in the default extension
            if os.path.isdir(file):
                for filename in recursive_iglob(os.path.join(file, f"*{DEFAULT_EXTENSION}")):
                    yield filename

            # Otherwise read the file as normal
            else:
                yield file
