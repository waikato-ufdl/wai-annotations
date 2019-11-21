import itertools
from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Generic, Iterator, Iterable, Dict, Any

from .external_formats import ExternalFormat
from ._ArgumentConsumer import ArgumentConsumer


class Reader(ArgumentConsumer, Generic[ExternalFormat]):
    """
    Base class for classes which can read a specific external format from disk.
    """
    def __init__(self, input: str):
        # The name of the input file or directory to read from
        self.input: str = input

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument(
            "-i", "--input", metavar="dir_or_file", dest="input", required=True,
            help=cls.input_help_text())

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        return {"input": namespace.input}

    def load(self) -> Iterator[ExternalFormat]:
        """
        Creates an iterator over the instances in the input file/directory.

        :return:            An iterator to the instances in the input file/directory.
        """
        return self.read_all(self.determine_input_files(self.input))

    @abstractmethod
    def determine_input_files(self, input_path: str) -> Iterable[str]:
        """
        Determines the input files from the provided input path.

        :param input_path:  The input path (directory or filename).
        :return:            An iterable of filenames.
        """
        pass

    @classmethod
    @abstractmethod
    def input_help_text(cls) -> str:
        """
        Gets the help text describing what type of path the 'input' option
        expects and how it is interpreted.

        :return:    The help text.
        """
        pass

    def read_all(self, filenames: Iterable[str]) -> Iterator[ExternalFormat]:
        """
        Reads instances from all of the given files.

        :param filenames:   The files to read from.
        :return:            An iterator to the instances in the files.
        """
        return itertools.chain(*map(self.read, filenames))

    @abstractmethod
    def read(self, filename: str) -> Iterator[ExternalFormat]:
        """
        Reads a number of instances from a given file. If the
        instance information is spread over multiple files, the
        other files should be inferable from either the given
        filename or the contents of that file.

        :param filename:    The name of the file to read.
        :return:            An iterator to the instances in that file.
        """
        pass
