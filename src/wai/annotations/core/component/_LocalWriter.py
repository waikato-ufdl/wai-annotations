from abc import abstractmethod
from os import mkdir, walk
from os.path import isdir, exists, join, basename, split, relpath, normpath
from tempfile import TemporaryDirectory
from typing import Iterable, Iterator, IO, Tuple, Optional

from wai.common.cli.options import TypedOption, Option

from ._Writer import Writer, ExternalFormat


class LocalWriter(Writer[ExternalFormat]):
    """
    Base class for classes which can write a specific external format to disk.
    """
    output = TypedOption("-o", "--output",
                         type=str,
                         metavar="dir_or_file", required=True)

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.output:
            return cls.output_help_text()

        return super().get_help_text_for_option(option)

    @classmethod
    @abstractmethod
    def output_help_text(cls) -> str:
        """
        Gets the help text describing what type of path the 'output' option
        expects and how it is interpreted.

        :return:    The help text.
        """
        pass

    def split_write(self, instances: Iterable[ExternalFormat], split_name: str):
        # Split the output into directory and filename
        if self.expects_file():
            path, filename = split(self.output)
        else:
            path, filename = self.output, ""

        # Check if the directory exists
        if not isdir(path):
            raise ValueError(f"{path} is not a directory, or does not exist")

        # Create a sub-directory for the split
        split_path = join(path, split_name)
        if not exists(split_path):
            mkdir(split_path)

        # Write the split
        self.write_to_path(instances, join(split_path, filename))

    def write(self, instances: Iterable[ExternalFormat]):
        self.write_to_path(instances, self.output)

    @abstractmethod
    def write_to_path(self, instances: Iterable[ExternalFormat], path: str):
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
        # Save the actual output directory
        actual_output = self.output

        try:
            # Create a temporary directory to write into
            with TemporaryDirectory() as temp_directory:
                # Determine the directory/path to write to
                self.output = temp_directory if not self.expects_file() else join(temp_directory, basename(self.output))

                # Write the instances to the temporary directory
                self.save(instances)

                # Iterate through all written files
                for dirpath, dirnames, filenames in walk(temp_directory):
                    for filename in filenames:
                        full_filename = normpath(join(relpath(dirpath, temp_directory), filename))
                        with open(join(temp_directory, full_filename), "rb") as file:
                            yield full_filename, file

        # Restore the original output value
        finally:
            self.output = actual_output
