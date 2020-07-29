import itertools
from abc import abstractmethod
from random import Random
from typing import Generic, Iterator, TypeVar

from wai.common.cli import CLIInstantiable
from wai.common.cli.options import TypedOption
from wai.common.iterate import random

from ..logging import StreamLogger, LoggingEnabled
from ..utils import chain_map

ExternalFormat = TypeVar("ExternalFormat")


class Reader(LoggingEnabled, CLIInstantiable, Generic[ExternalFormat]):
    """
    Base class for classes which can read a specific external format.
    """
    # The seed to use for randomisation of the read sequence
    seed = TypedOption(
        "--seed",
        type=int,
        help="the seed to use for randomising the read sequence"
    )

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

    @abstractmethod
    def get_annotation_files(self) -> Iterator[str]:
        """
        Gets an iterator over the annotation files that will be
        read by this reader.

        :return:    The iterator of file-names.
        """
        pass

    @abstractmethod
    def get_negative_files(self) -> Iterator[str]:
        """
        Gets an iterator over the negative images that will be
        read by this reader.

        :return:    The iterator of file-names.
        """
        pass

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
