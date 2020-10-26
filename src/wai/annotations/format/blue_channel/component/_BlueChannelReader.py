import os
from PIL import Image as PILImage

from ....core.stream import ThenFunction
from ....domain.image import Image, ImageFormat
from ....domain.image.util import get_associated_image
from ....domain.image.segmentation.util import ImageSegmentationReader
from ..util import BlueChannelFormat


class BlueChannelReader(ImageSegmentationReader[BlueChannelFormat]):
    """
    Reader of image-segmentation data-sets which store annotations
    in the blue-channel of an image.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[BlueChannelFormat]):
        # Get the path to the data-file
        data_path = self.get_data_path(filename)

        # Get the associated data image
        data_image_filename = get_associated_image(
            os.path.join(data_path, os.path.splitext(os.path.basename(filename))[0]),
            [ImageFormat.JPG, ImageFormat.BMP, ImageFormat.PNG]
        )

        # If the data image found was the annotations image, throw an error
        if data_image_filename is None or os.path.normpath(data_image_filename) == os.path.normpath(filename):
            raise Exception(f"Couldn't find data-image associated with {filename}")

        then(
            BlueChannelFormat(
                Image.from_file(data_image_filename),
                PILImage.open(filename)
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[BlueChannelFormat]):
        then(
            BlueChannelFormat(
                Image.from_file(filename),
                None
            )
        )
