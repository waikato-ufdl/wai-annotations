import os
from PIL import Image
from typing import Iterator

from ....domain.image import ImageInfo, ImageFormat
from ....domain.image.util import get_associated_image
from ....domain.image.segmentation.util import ImageSegmentationReader
from .._format import IndexedPNGFormat


class IndexedPNGReader(ImageSegmentationReader[IndexedPNGFormat]):
    """
    Reader of image-segmentation data-sets which store annotations
    in an indexed PNG image.
    """
    def read_annotation_file(self, filename: str) -> Iterator[IndexedPNGFormat]:
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

        yield IndexedPNGFormat(
            ImageInfo.from_file(data_image_filename),
            Image.open(filename)
        )

    def read_negative_file(self, filename: str) -> Iterator[IndexedPNGFormat]:
        yield IndexedPNGFormat(
            ImageInfo.from_file(filename),
            None
        )
