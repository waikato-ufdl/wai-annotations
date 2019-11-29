import os
from typing import Iterable

from ...core import SeparateImageWriter, ImageInfo
from ...core.external_formats import VGGExternalFormat
from ...vgg_utils.configuration import VGGFile


class VGGWriter(SeparateImageWriter[VGGExternalFormat]):
    """
    Writer of VGG-format JSON files.
    """
    @classmethod
    def output_help_text(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"

    def write_without_images(self, instances: Iterable[VGGExternalFormat], path: str):
        # Create a map of images
        images = {}

        # Determine the directory for images
        path = os.path.dirname(self.output)

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
