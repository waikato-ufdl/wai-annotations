from typing import Iterable

from ....core.component import JSONWriter
from ....domain.image import ImageInfo
from ..configuration import VGGFile
from .._format import VGGExternalFormat


class VGGWriter(JSONWriter[VGGExternalFormat]):
    """
    Writer of VGG-format JSON files.
    """
    def create_json_object(self, instances: Iterable[VGGExternalFormat]) -> VGGFile:
        # Create a map of images
        images = {}

        # Write each instance
        for instance_index, instance in enumerate(instances, 1):
            # Unpack the instance
            image_info, image = instance

            # Add the image to the map
            images[f"{image.filename}-1"] = image

        return VGGFile(**images)

    def extract_file_info_from_external_format(self, instance: VGGExternalFormat) -> ImageInfo:
        # Unpack the instance
        image_info, image = instance

        return image_info

    @classmethod
    def output_help_text(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"
