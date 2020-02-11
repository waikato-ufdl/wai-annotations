import os
from abc import ABC, abstractmethod
from typing import Iterable

from ._typing import ExternalFormat
from ._Writer import Writer


class SeparateImageWriter(Writer[ExternalFormat], ABC):
    """
    Writer for external formats where the image is stored separately
    to the annotations.
    """
    def __init__(self, output: str, no_images: bool = False):
        super().__init__(output)

        self.no_images: bool = no_images

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
