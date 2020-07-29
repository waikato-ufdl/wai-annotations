import os
from abc import ABC, abstractmethod
from typing import Iterable, TypeVar

from wai.common.cli.options import FlagOption

from ..stream import InlineStreamProcessor
from ._LocalWriter import LocalWriter

ExternalFormat = TypeVar("ExternalFormat")


class InlineFileWriter(InlineStreamProcessor[ExternalFormat]):
    """
    Writes the files to disk.
    """
    def __init__(self, writer: 'SeparateFileWriter', path: str):
        self._writer: 'SeparateFileWriter' = writer
        self._path: str = path

    def _process_element(self, element: ExternalFormat) -> Iterable[ExternalFormat]:
        # Get the file info from the instance
        file_info = self._writer.extract_file_info_from_external_format(element)

        # Get the path to write the file to
        path = self._path if os.path.isdir(self._path) else os.path.dirname(self._path)

        # Write the file
        file_info.write_data_if_present(path)

        return element,


class SeparateFileWriter(LocalWriter[ExternalFormat], ABC):
    """
    Writer for external formats where the file is stored separately
    to the annotations.
    """
    annotations_only = FlagOption("--annotations-only",
                                  help="skip the writing of data files, outputting only the annotation files")

    def write_to_path(self, instances: Iterable[ExternalFormat], path: str):
        # Wrap the instances with an inline file writer if writing files
        if not self.annotations_only:
            instances = InlineFileWriter(self, path).process(instances)

        self.write_annotations_only(instances, path)

    @abstractmethod
    def write_annotations_only(self, instances: Iterable[ExternalFormat], path: str):
        """
        Writes the annotations for a series of instances to disk. The data files
        are assumed already written.

        :param instances:   The instances to write to disk.
        :param path:        The path to write the instances to. Can be a directory
                            or a specific filename depending on the disk-format
                            of the external format.
        """
        pass
