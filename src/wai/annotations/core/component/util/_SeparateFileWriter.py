import os
from abc import ABC
from typing import Optional

from wai.common.cli.options import FlagOption, Option

from ...domain import Data
from ._LocalFileWriter import LocalFileWriter, ElementType


class SeparateFileWriter(LocalFileWriter[ElementType], ABC):
    """
    Writer for external formats where the file is stored separately
    to the annotations.
    """
    # Whether to only output the annotations files
    annotations_only = FlagOption(
        "--annotations-only"
    )

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.annotations_only:
            return cls.get_help_text_for_annotations_only_option()
        return super().get_help_text_for_option(option)

    @classmethod
    def get_help_text_for_annotations_only_option(cls) -> str:
        """
        Returns the help text for the '--annotations-only' option.
        """
        return "skip the writing of data files, outputting only the annotation files"

    def write_data_file(self, data_file: Data, path: str):
        """
        Writes the data-file to disk.

        :param data_file:   The data-file to write.
        :param path:        The path to write the file to.
        """
        if not self.annotations_only:
            data_file.write_data_if_present(path)
