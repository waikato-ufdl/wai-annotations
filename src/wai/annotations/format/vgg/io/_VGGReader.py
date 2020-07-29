import os
from typing import Iterator

from ....core.component import LocalReader
from ....domain.image import ImageInfo
from ..configuration import VGGFile, Image, FileAttributes
from .._format import VGGExternalFormat


class VGGReader(LocalReader[VGGExternalFormat]):
    """
    Reader of VGG-format JSON files.
    """
    def read_annotation_file(self, filename: str) -> Iterator[VGGExternalFormat]:
        # Read in the file
        vgg_file: VGGFile = VGGFile.load_json_from_file(filename)

        # Create the path to the directory
        path = os.path.dirname(filename)

        # Each image yields an instance
        for key in vgg_file:
            # Get the image
            image = vgg_file[key]

            # Get the image associated to this entry
            image_file = os.path.join(path, image.filename)

            # Load the image
            image_data = None
            if os.path.exists(image_file):
                with open(image_file, "rb") as file:
                    image_data = file.read()

            yield ImageInfo(image.filename, image_data), image

    def read_negative_file(self, filename: str) -> Iterator[VGGExternalFormat]:
        image_info = ImageInfo.from_file(filename)

        yield image_info, Image(filename=image_info.filename,
                                size=-1,
                                file_attributes=FileAttributes(caption="", public_domain="no", image_url=""),
                                regions=[])
