import os
from abc import ABC, abstractmethod
from typing import Iterable

from wai.common.cli.options import FlagOption

from ..stream import InlineStreamProcessor
from .._typing import ExternalFormat
from ._Writer import Writer


class InlineImageWriter(InlineStreamProcessor[ExternalFormat]):
    """
    Writes the image from an instance to disk.
    """
    def __init__(self, writer: 'SeparateImageWriter', path: str):
        self._writer: 'SeparateImageWriter' = writer
        self._path: str = path

    def _process_element(self, element: ExternalFormat) -> Iterable[ExternalFormat]:
        # Get the image info from the instance
        image_info = self._writer.extract_image_info_from_external_format(element)

        # Get the path to write the image to
        path = self._path if os.path.isdir(self._path) else os.path.dirname(self._path)

        # Write the image
        image_info.write_data_if_present(path)

        return element,


class SeparateImageWriter(Writer[ExternalFormat], ABC):
    """
    Writer for external formats where the image is stored separately
    to the annotations.
    """
    no_images = FlagOption("--no-images",
                           help="skip the writing of images, outputting only the annotation files")

    def write(self, instances: Iterable[ExternalFormat], path: str):
        # Wrap the instances with an image writer if writing images
        if not self.no_images:
            instances = InlineImageWriter(self, path).process(instances)

        self.write_without_images(instances, path)

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
