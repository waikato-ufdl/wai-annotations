from abc import ABC
from argparse import ArgumentParser, Namespace
import re
from typing import Dict, Any

from .._InternalFormatConverter import InternalFormatConverter
from ._CommandLineConverterFactory import CommandLineConverterFactory


class CommandLineInternalFormatConverterFactory(CommandLineConverterFactory[InternalFormatConverter], ABC):
    """
    Base class for command-line factories that produce internal-format converters.
    """
    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument(
            "-l", "--labels", metavar="label1,label2,...", dest="labels", required=False,
            help="comma-separated list of labels to use", default="")

        parser.add_argument(
            "-r", "--regexp", metavar="regexp", dest="regexp", required=False,
            help="regular expression for using only a subset of labels", default="")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        # Parse the labels
        labels = list(namespace.labels.split(",")) if len(namespace.labels) > 0 else None

        # Parse the regex
        regex = re.compile(namespace.regexp) if len(namespace.regexp) > 0 else None

        return {"labels": labels, "regex": regex}
