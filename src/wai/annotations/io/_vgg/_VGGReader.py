import os
from typing import Iterator, Iterable

from ...core import Reader, ImageInfo
from ...core.external_formats import VGGExternalFormat
from ...vgg_utils.configuration import VGGFile


class VGGReader(Reader[VGGExternalFormat]):
    """
    Reader of VGG-format JSON files.
    """
    def determine_input_files(self, input_path: str) -> Iterable[str]:
        return input_path,

    @classmethod
    def input_help_text(cls) -> str:
        return "JSON-format VGG annotations file"

    def read(self, filename: str) -> Iterator[VGGExternalFormat]:
        # Read in the file
        vgg_file: VGGFile = VGGFile.load_from_json_file(filename)

        # Create the path to the directory
        path = os.path.dirname(filename)

        # Each image yields an instance
        for image in vgg_file._additional_properties.values():
            # Get the image associated to this entry
            image_file = os.path.join(path, image.filename)

            # Load the image
            image_data = None
            if os.path.exists(image_file):
                with open(image_file, "rb") as file:
                    image_data = file.read()

            yield ImageInfo(image.filename, image_data), image
