import itertools
from abc import ABC
from argparse import Namespace
from typing import Iterator, List, Union

from wai.common.cli import OptionsList
from wai.common.cli.options import TypedOption

from ..utils import chain_map, recursive_iglob, read_file_list
from ._Reader import Reader, ExternalFormat


class LocalReader(Reader[ExternalFormat], ABC):
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

    def __init__(self, namespace: Union[Namespace, OptionsList, None] = None):
        super().__init__(namespace)

        # Warn the user if no input files were specified
        if len(self.inputs) + len(self.negatives) + len(self.input_files) + len(self.negative_files) == 0:
            self.logger.warning("No input files selected to convert")

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
