import os
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Dict, Any, Iterable

from .external_formats import ExternalFormat
from ._Writer import Writer
from ._ImageInfo import ImageInfo


class SeparateImageWriter(Writer[ExternalFormat], ABC):
    """
    Writer for external formats where the image is stored separately
    to the annotations.
    """
    def __init__(self, output: str, no_images: bool = False):
        super().__init__(output)

        self.no_images: bool = no_images

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument("--no-images", action="store_true", required=False, dest="no_images",
                            help="skip the writing of images, outputting only the report files")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(no_images=namespace.no_images)
        return kwargs

    def write(self, instances: Iterable[ExternalFormat], path: str):
        self.write_without_images(map(self.inline_image_writer, instances), path)

    @abstractmethod
    def write_without_images(self, instances: Iterable[ExternalFormat], path: str):
        """
        Writes a series of instances to disk. The images are
        assumed to be already written.

        :param instances:   The instances to write to disk.
        :param path:        The path to write the instances to. Can be a directory
                            or a specific filename depending on the disk-format
                            of the external format.
        """
        pass

    @abstractmethod
    def extract_image_info_from_external_format(self, instance: ExternalFormat) -> ImageInfo:
        """
        Extracts an image-info object from the external format of this writer.

        :param instance:    The instance being written.
        :return:            The image info for the instance.
        """
        pass

    def inline_image_writer(self, instance: ExternalFormat) -> ExternalFormat:
        """
        Writes images from the pipeline as they are processed.

        :param instance:    An instance in the pipeline.
        :return:            The same instance.
        """
        # If --no-images is set, skip
        if self.no_images:
            return instance

        # Get the image info from the instance
        image_info = self.extract_image_info_from_external_format(instance)

        # Get the path to write the image to
        path = self.output if os.path.isdir(self.output) else os.path.dirname(self.output)

        # Write the image
        image_info.write_data_if_present(path)

        return instance
