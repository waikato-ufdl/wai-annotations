import itertools
from abc import abstractmethod
from argparse import Namespace
from typing import Generic, Iterator, List, Union

from wai.common.cli import CLIInstantiable, OptionsList
from wai.common.cli.options import TypedOption

from .logging import StreamLogger, LoggingEnabled
from .utils import chain_map, recursive_iglob, read_file_list
from ._ImageInfo import ImageInfo
from ._typing import ExternalFormat


class Reader(LoggingEnabled, CLIInstantiable, Generic[ExternalFormat]):
    """
    Base class for classes which can read a specific external format from disk.
    """
    # The name of the input annotation files to read from
    inputs: List[str] = TypedOption(
        "-i", "--inputs",
        type=str,
        metavar="files", action="append",
        help="Input annotations files (can use glob syntax)"
    )

    # The names of images to include in the conversion without annotations
    negatives: List[str] = TypedOption(
        "-n", "--negatives",
        type=str,
        metavar="image", action="append",
        help="Image files that have no annotations (can use glob syntax)"
    )

    # The names of files to load input lists from
    input_files: List[str] = TypedOption(
        "-I", "--input-files",
        type=str,
        action="append",
        help="Files containing lists of input annotation files (can use glob syntax)"
    )

    # The names of files to load negative lists from
    negative_files: List[str] = TypedOption(
        "-N", "--negative-files",
        type=str,
        action="append",
        help="Files containing lists of negative images (can use glob syntax)"
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
        # Create a stream processor to log when we are loading a file
        stream_log = StreamLogger(self.logger.info, lambda instance: f"Loading file {instance}").process

        return itertools.chain(
            chain_map(self.read_annotation_file, stream_log(self.annotation_files())),
            chain_map(self.read_negative_image_file, stream_log(self.negative_image_files()))
        )

    def annotation_files(self) -> Iterator[str]:
        """
        Gets an iterator over the annotation files that will be
        read by this reader based on the input options.

        :return:    The iterator of filenames.
        """
        return itertools.chain(
            chain_map(recursive_iglob, self.inputs),
            chain_map(read_file_list, chain_map(recursive_iglob, self.input_files))
        )

    def negative_image_files(self) -> Iterator[str]:
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

    def read_negative_image_file(self, filename: str) -> Iterator[ExternalFormat]:
        """
        Reads an image file as a negative (contains no annotations).

        :param filename:    The name of the image file.
        :return:            An iterator to the negative instance.
        """
        # Attempt to read in the image data
        image_info = ImageInfo.from_file(filename)

        yield self.image_info_to_external_format(image_info)

    @abstractmethod
    def image_info_to_external_format(self, image_info: ImageInfo) -> ExternalFormat:
        """
        Converts an image-info object for a negative image
        into the external format.

        :param image_info:  The image info object to convert.
        :return:            The external format instance.
        """
        pass
