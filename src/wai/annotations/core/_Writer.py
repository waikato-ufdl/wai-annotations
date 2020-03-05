from abc import abstractmethod
from os import listdir
from os.path import isdir, dirname, join
from tempfile import TemporaryDirectory
from typing import Generic, Iterable, Iterator, IO, Tuple

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

        # Check if the directory exists
        path = self.output
        if self.expects_file():
            path = dirname(path)
        if not isdir(path):
            raise ValueError(f"{path} is not a directory, or does not exist")

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
    def expects_file(self) -> bool:
        """
        Whether this writer expects the output parameter to be a file.

        :return:    True if the writer expects a file,
                    False if it expects a directory.
        """
        pass

    def file_iterator(self, instances: Iterable[ExternalFormat]) -> Iterator[Tuple[str, IO[bytes]]]:
        """
        Converts a series of instances into the files they are written to.
        No files are actually written.

        N.B. Some files are written, but to a temporary directory which is
        removed on iterator completion.

        :param instances:   The instances to write.
        :return:            An iterator of filename, file-contents pairs.
        """
        # Create a temporary directory to write into
        with TemporaryDirectory() as dir:
            # Determine the directory/path to write to
            path = dir if not self.expects_file() else join(dir, "annotations")

            # Write the instances to the temporary directory
            self.write(instances, path)

            # Iterate through all written files
            for filename in listdir(dir):
                with open(join(dir, filename), "rb") as file:
                    yield filename, file

    @abstractmethod
    def extract_image_info_from_external_format(self, instance: ExternalFormat) -> ImageInfo:
        """
        Extracts an image-info object from the external format of this writer.

        :param instance:    The instance being written.
        :return:            The image info for the instance.
        """
        pass
