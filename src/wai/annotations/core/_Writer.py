from abc import abstractmethod
from typing import Generic, Iterable

from .logging import LoggingEnabled, StreamLogger
from ._ImageInfo import ImageInfo
from ._typing import ExternalFormat


class Writer(LoggingEnabled, Generic[ExternalFormat]):
    """
    Base class for classes which can write a specific external format to disk.
    """
    def __init__(self, output: str):
        super().__init__()

        # The output file/directory to write the converted data-set to
        self.output: str = output

    def save(self, instances: Iterable[ExternalFormat]):
        """
        Writes a series of instances to disk.

        :param instances:   The instances to write to disk.
        """
        # Create a stream processor to log when we are writing a file
        stream_log = StreamLogger(
            self.logger.info,
            lambda instance:
            f"Saving annotations for "
            f"{self.extract_image_info_from_external_format(instance).filename}").process

        self.write(stream_log(instances), self.output)

    @abstractmethod
    def write(self, instances: Iterable[ExternalFormat], path: str):
        """
        Writes a series of instances to disk.

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
