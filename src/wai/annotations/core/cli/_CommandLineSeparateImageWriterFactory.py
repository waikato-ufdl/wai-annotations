from abc import ABC
from argparse import ArgumentParser, Namespace
from typing import Dict, Any

from .._SeparateImageWriter import SeparateImageWriter
from ._CommandLineWriterFactory import CommandLineWriterFactory


class CommandLineSeparateImageWriterFactory(CommandLineWriterFactory[SeparateImageWriter], ABC):
    """
    Base class for command-line factories that produce separate-image writers.
    """
    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument("--no-images", action="store_true", required=False, dest="no_images",
                            help="skip the writing of images, outputting only the report files")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(no_images=namespace.no_images)
        return kwargs
