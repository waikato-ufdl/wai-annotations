import os
from abc import ABC
from typing import Tuple

from wai.common.cli import OptionValueHandler
from wai.common.cli.options import TypedOption


class LabelSeparatorMixin(OptionValueHandler, ABC):
    """
    Mixin which adds the label-separator option/utilities to
    a class.
    """
    # A separator to look for/insert between the base filename and the label
    label_separator: str = TypedOption(
        "--label-separator",
        type=str,
        default="-",
        metavar="SEPARATOR",
        help="the separator between the base filename and the label"
    )

    def format_filename_with_label(self, filename: str, label: str) -> str:
        """
        Formats a filename with the label appended before the extension.

        :param filename:    The base filename to format.
        :param label:       The label to append to the filename.
        :return:            The formatted filename, with label.
        """
        # Get the base filename and extension separated
        base_filename, extension = os.path.splitext(filename)

        return f"{base_filename}{self.label_separator}{label}{extension}"

    def parse_filename(self, filename: str) -> Tuple[str, str]:
        """
        Parses a filename with a label suffix into its constituent
        base filename/label parts.

        :param filename:    The filename to parse.
        :return:            The base filename (without extension) and the label.
        """
        # Remove the extension
        filename_no_ext = os.path.splitext(filename)[0]

        return tuple(filename_no_ext.rsplit(self.label_separator, 1))
