import os
from argparse import ArgumentParser, Namespace
from typing import Iterable, Any, Dict

from ...core import Writer
from ...core.external_formats import VGGExternalFormat
from ...vgg_utils.configuration import VGGFile


class VGGWriter(Writer[VGGExternalFormat]):
    """
    Writer of VGG-format JSON files.
    """
    def __init__(self, output: str, no_images: bool = False):
        super().__init__(output)

        self.no_images: bool = no_images

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument("--no-images", action="store_true", required=False, dest="no_images",
                            help="skip the writing of images, outputting only the annotations")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(no_images=namespace.no_images)
        return kwargs

    @classmethod
    def output_help_text(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"

    def write(self, instances: Iterable[VGGExternalFormat], path: str):
        # Create a map of images
        images = {}

        # Determine the directory for images
        path = os.path.dirname(self.output)

        # Write each instance
        for instance_index, instance in enumerate(instances, 1):
            # Unpack the instance
            image_info, image = instance

            # Write the image
            if not self.no_images:
                image_info.write_data_if_present(path)

            # Add the image to the map
            images[f"{image.filename}-1"] = image

        # Save the file
        VGGFile(**images).save_to_json_file(self.output)
