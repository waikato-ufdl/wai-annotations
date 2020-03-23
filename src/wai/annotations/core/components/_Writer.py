from abc import abstractmethod
from os import mkdir, walk
from os.path import isdir, exists, join, basename, split, relpath
from tempfile import TemporaryDirectory
from typing import Generic, Iterable, Iterator, IO, Tuple, Optional

from wai.bynning.operations import split as bynning_split_op

from wai.common.cli import CLIInstantiable
from wai.common.cli.options import TypedOption, Option

from ..logging import LoggingEnabled, StreamLogger
from .._ImageInfo import ImageInfo
from .._typing import ExternalFormat


class Writer(LoggingEnabled, CLIInstantiable, Generic[ExternalFormat]):
    """
    Base class for classes which can write a specific external format to disk.
    """
    output = TypedOption("-o", "--output",
                         type=str,
                         metavar="dir_or_file", required=True)

    split_names = TypedOption("--split-names",
                              type=str,
                              metavar="SPLIT NAME",
                              nargs="+",
                              help="the names to use for the splits")

    split_ratios = TypedOption("--split-ratios",
                               type=int,
                               metavar="RATIO",
                               nargs="+",
                               help="the ratios to use for the splits")

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.output:
            return cls.output_help_text()

        return None

    @classmethod
    @abstractmethod
    def output_help_text(cls) -> str:
        """
        Gets the help text describing what type of path the 'output' option
        expects and how it is interpreted.

        :return:    The help text.
        """
        pass

    def save(self, instances: Iterable[ExternalFormat]):
        """
        Writes a series of instances to disk.

        :param instances:   The instances to write to disk.
        """
        self.split_write(instances, self.output)

    def split_write(self, instances: Iterable[ExternalFormat], path: str):
        """
        Writes a series of instances to disk. Performs splitting if configured.

        :param instances:   The instances to write to disk.
        :param path:        The path to write the instances to. Can be a directory
                            or a specific filename depending on the disk-format
                            of the external format.
        """
        # Create a stream processor to log when we are writing a file
        stream_logger = StreamLogger(
            self.logger.info,
            lambda instance:
            f"Saving annotations for "
            f"{self.extract_image_info_from_external_format(instance).filename}")

        # Wrap the stream with the logger
        instances = stream_logger.process(instances)

        # Split the output into directory and filename
        if self.expects_file():
            path, filename = split(path)
        else:
            path, filename = path, ""

        # Check if the directory exists
        if not isdir(path):
            raise ValueError(f"{path} is not a directory, or does not exist")

        # If creating a split, defer to wai.bynning
        if len(self.split_names) != 0 and len(self.split_ratios) != 0:
            # Split and iterate through the instances for the split
            for split_name, split_instances in bynning_split_op(
                    instances,
                    **{split_name: split_ratio
                       for split_name, split_ratio
                       in zip(self.split_names, self.split_ratios)}
            ).items():
                # Create a sub-directory for the split
                split_path = join(path, split_name)
                if not exists(split_path):
                    mkdir(split_path)

                # Write the split
                self.write(split_instances, join(split_path, filename))

        # Otherwise just write the instances
        else:
            self.write(instances, join(path, filename))

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
            path = dir if not self.expects_file() else join(dir, basename(self.output))

            # Write the instances to the temporary directory
            self.split_write(instances, path)

            # Iterate through all written files
            for dirpath, dirnames, filenames in walk(dir):
                for filename in filenames:
                    full_filename = join(relpath(dirpath, dir), filename)
                    with open(join(dir, full_filename), "rb") as file:
                        yield full_filename, file

    @abstractmethod
    def extract_image_info_from_external_format(self, instance: ExternalFormat) -> ImageInfo:
        """
        Extracts an image-info object from the external format of this writer.

        :param instance:    The instance being written.
        :return:            The image info for the instance.
        """
        pass
