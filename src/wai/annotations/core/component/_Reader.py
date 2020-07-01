import itertools
from abc import abstractmethod
from argparse import Namespace
from random import Random
from typing import Generic, Iterator, List, Union, TypeVar

from wai.common.cli import CLIInstantiable, OptionsList
from wai.common.cli.options import TypedOption
from wai.common.iterate import random

from ..logging import StreamLogger, LoggingEnabled
from ..utils import chain_map, recursive_iglob, read_file_list
from ..instance import FileInfo

ExternalFormat = TypeVar("ExternalFormat")


class Reader(LoggingEnabled, CLIInstantiable, Generic[ExternalFormat]):
    """
    Base class for classes which can read a specific external format from disk.
    """
    # The name of the input annotation files to read from
    inputs: List[str] = TypedOption(
        "-i", "--inputs",
        type=str,
        metavar="files", action="concat",
        help="Input annotations files (can use glob syntax)"
    )

    # The names of files to include in the conversion without annotations
    negatives: List[str] = TypedOption(
        "-n", "--negatives",
        type=str,
        metavar="file", action="concat",
        help="Files that have no annotations (can use glob syntax)"
    )

    # The names of files to load input lists from
    input_files: List[str] = TypedOption(
        "-I", "--input-files",
        type=str,
        action="concat",
        help="Files containing lists of input annotation files (can use glob syntax)"
    )

    # The names of files to load negative lists from
    negative_files: List[str] = TypedOption(
        "-N", "--negative-files",
        type=str,
        action="concat",
        help="Files containing lists of negative files (can use glob syntax)"
    )

    # The seed to use for randomisation of the read sequence
    seed = TypedOption(
        "--seed",
        type=int,
        help="the seed to use for randomising the read sequence"
    )

    def __init__(self, namespace: Union[Namespace, OptionsList, None] = None):
        super().__init__(namespace)

        # Warn the user if no input files were specified
        if len(self.inputs) + len(self.negatives) + len(self.input_files) + len(self.negative_files) == 0:
            self.logger.warning("No input files selected to convert")

    def load(self) -> Iterator[ExternalFormat]:
        """
        Creates an iterator over the instances in the input file/directory.

        :return:            An iterator to the instances in the input file/directory.
        """
        # Get the annotations and negative files to read
        annotation_files = self.get_annotation_files()
        negative_files = self.get_negative_files()

        # If a seed is given, randomise the file order
        if self.seed is not None:
            r = Random(self.seed)
            annotation_files = random(annotation_files, r)
            negative_files = random(negative_files, r)

        # Create a stream processor to log when we are loading a file
        stream_logger = StreamLogger(self.logger.info, lambda instance: f"Loading file {instance}")
        annotation_files = stream_logger.process(annotation_files)
        negative_files = stream_logger.process(negative_files)

        return itertools.chain(
            chain_map(self.read_annotation_file, annotation_files),
            chain_map(self.read_negative_file, negative_files)
        )

    def get_annotation_files(self) -> Iterator[str]:
        """
        Gets an iterator over the annotation files that will be
        read by this reader based on the input options.

        :return:    The iterator of filenames.
        """
        return itertools.chain(
            chain_map(recursive_iglob, self.inputs),
            chain_map(read_file_list, chain_map(recursive_iglob, self.input_files))
        )

    def get_negative_files(self) -> Iterator[str]:
        """
        Gets an iterator over the negative images that will be
        read by this reader based on the input options.

        :return:    The iterator of filenames.
        """
        return itertools.chain(
            chain_map(recursive_iglob, self.negatives),
            chain_map(read_file_list, chain_map(recursive_iglob, self.negative_files))
        )

    @abstractmethod
    def read_annotation_file(self, filename: str) -> Iterator[ExternalFormat]:
        """
        Reads a number of instances from a given file. If the
        instance information is spread over multiple files, the
        other files should be inferable from either the given
        filename or the contents of that file.

        :param filename:    The name of the file to read.
        :return:            An iterator to the instances in that file.
        """
        pass

    @abstractmethod
    def read_negative_file(self, filename: str) -> Iterator[ExternalFormat]:
        """
        Reads an image file as a negative (contains no annotations).

        :param filename:    The name of the image file.
        :return:            An iterator to the negative instance.
        """
        pass
