import os

from wai.common.cli.options import TypedOption
from wai.common.file.report import loadf, Report

from .....core.component.util import AnnotationFileProcessor
from .....core.stream import ThenFunction
from .....domain.image import Image, ImageFormat
from .....domain.image.util import get_associated_image
from ...util import ADAMSExternalFormat


class ADAMSBaseReader(AnnotationFileProcessor[ADAMSExternalFormat]):
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

    def read_annotation_file(self, filename: str, then: ThenFunction[ADAMSExternalFormat]):
        # Get the image associated to this report
        image_file = get_associated_image(os.path.splitext(filename)[0], self.image_format_preference_order)

        # Make sure an image file was found
        if image_file is None:
            raise ValueError(f"No associated image found for {filename}")

        # Create the image info object
        image_info = Image.from_file(image_file)

        # Load the report
        report: Report = loadf(filename)

        then((image_info, report))

    def read_negative_file(self, filename: str, then: ThenFunction[ADAMSExternalFormat]):
        then((Image.from_file(filename), None))
