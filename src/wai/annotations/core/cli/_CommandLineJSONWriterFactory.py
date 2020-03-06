from abc import ABC
from argparse import ArgumentParser, Namespace
from typing import Dict, Any

from ._CommandLineSeparateImageWriterFactory import CommandLineSeparateImageWriterFactory


class CommandLineJSONWriterFactory(CommandLineSeparateImageWriterFactory, ABC):
    """
    Base class for command-line factories that produce JSON writers.
    """
    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument("--pretty", action="store_true", dest="pretty",
                            help="whether to pretty-print the output")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(pretty=namespace.pretty)
        return kwargs
