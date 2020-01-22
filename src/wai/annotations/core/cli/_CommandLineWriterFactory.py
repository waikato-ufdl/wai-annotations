from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Dict, Any, TypeVar

from .._Writer import Writer
from ._CommandLineFactory import CommandLineFactory

# Type variable for the related writer class that this factory produces
RelatedWriterClass = TypeVar("RelatedWriterClass", bound=Writer)


class CommandLineWriterFactory(CommandLineFactory[RelatedWriterClass], ABC):
    """
    Base class for command-line factories that produce writers.
    """
    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument(
            "-o", "--output", metavar="dir_or_file", dest="output", required=True,
            help=cls.output_help_text())

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        return {"output": namespace.output}

    @classmethod
    @abstractmethod
    def output_help_text(cls) -> str:
        """
        Gets the help text describing what type of path the 'output' option
        expects and how it is interpreted.

        :return:    The help text.
        """
        pass
