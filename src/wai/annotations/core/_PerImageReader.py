import os
import re
from abc import abstractmethod
from argparse import Namespace, ArgumentParser
from typing import Iterable, Pattern, Any, Dict

from .external_formats import ExternalFormat
from .utils import get_files_from_directory
from ._Reader import Reader


class PerImageReader(Reader[ExternalFormat]):
    """
    Base reader class for formats where each image file
    has its own annotations file.
    """
    def __init__(self, input: str, regex: Pattern):
        super().__init__(input)

        self.regex: Pattern = regex

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument(
            "-r", "--regexp", metavar="regexp", dest="regexp", required=False,
            help="regular expression for matching annotation files", default="")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(
            regex=re.compile(namespace.regexp if len(namespace.regexp) > 0 else cls.get_default_file_regex())
        )
        return kwargs

    def determine_input_files(self, input_path: str) -> Iterable[str]:
        # If given a directory as input, recursively load all
        # report files in the directory
        if os.path.isdir(input_path):
            return get_files_from_directory(input_path, self.regex)

        # Otherwise we expect a file containing a list of reports
        else:
            with open(input_path, "r") as file:
                return (line.strip() for line in file)

    @classmethod
    @abstractmethod
    def get_default_file_regex(cls) -> str:
        """
        Gets the default file matcher for annotation files
        for this format.

        :return:    The regex for matching annotation filenames.
        """
        pass
