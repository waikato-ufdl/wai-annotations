import os
from typing import Optional, Tuple

from .utils import get_image_size
from ._ImageFormat import ImageFormat


class ImageInfo:
    """
    Contains the information about the image a set of annotations
    belongs to.
    """
    def __init__(self,
                 filename: str,
                 data: Optional[bytes] = None,
                 format: Optional[ImageFormat] = None,
                 size: Optional[Tuple[int, int]] = None):
        self.filename: str = filename
        self.data: Optional[bytes] = data
        self.format: ImageFormat = format if format is not None else ImageFormat.for_filename(filename)
        self.size: Optional[Tuple[int, int]] = size if size is not None \
            else get_image_size(data) if data is not None \
            else None

    def width(self) -> int:
        """
        Gets the width of the image.

        :return:    The image width.
        """
        return self.size[0] if self.size is not None else -1

    def height(self) -> int:
        """
        Gets the height of the image.

        :return:    The image height.
        """
        return self.size[1] if self.size is not None else -1

    def write_data_if_present(self, path: str):
        """
        Writes the image data to disk under its filename in the given path.

        :param path:    The directory to write the image into.
        """
        if self.data is not None:
            with open(os.path.join(path, self.filename), "wb") as file:
                file.write(self.data)
