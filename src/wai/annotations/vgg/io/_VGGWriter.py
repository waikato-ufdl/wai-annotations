from typing import Iterable

from ...core import SeparateImageWriter, ImageInfo
from ..configuration import VGGFile
from .._format import VGGExternalFormat


class VGGWriter(SeparateImageWriter[VGGExternalFormat]):
    """
    Writer of VGG-format JSON files.
    """
    def __init__(self, output: str, no_images: bool = False, pretty: bool = False):
        super().__init__(output, no_images)

        self._pretty: bool = pretty

    def write_without_images(self, instances: Iterable[VGGExternalFormat], path: str):
        # Create a map of images
        images = {}

        # Write each instance
        for instance_index, instance in enumerate(instances, 1):
            # Unpack the instance
            image_info, image = instance

            # Add the image to the map
            images[f"{image.filename}-1"] = image

        # Save the file
        VGGFile(**images).save_json_to_file(path, 2 if self._pretty else None)

    def extract_image_info_from_external_format(self, instance: VGGExternalFormat) -> ImageInfo:
        # Unpack the instance
        image_info, image = instance

        return image_info

    def expects_file(self) -> bool:
        return True
