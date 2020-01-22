from typing import Iterable

from ...core import SeparateImageWriter, ImageInfo
from ..configuration import VGGFile
from .._format import VGGExternalFormat


class VGGWriter(SeparateImageWriter[VGGExternalFormat]):
    """
    Writer of VGG-format JSON files.
    """
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
        VGGFile(**images).save_to_json_file(self.output)

    def extract_image_info_from_external_format(self, instance: VGGExternalFormat) -> ImageInfo:
        # Unpack the instance
        image_info, image = instance

        return image_info
