from abc import ABC
from argparse import ArgumentParser, Namespace
from typing import Dict, Any

from .._Reader import Reader
from ._CommandLineFactory import CommandLineFactory


class CommandLineReaderFactory(CommandLineFactory[Reader], ABC):
    """
    Base class for command-line factories that produce readers.
    """
    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument(
            "-i", "--inputs", metavar="files", dest="inputs", required=True, action="append",
            help="Input image/annotations files (can use glob syntax)")
        parser.add_argument(
            "-n", "--negatives", metavar="image", dest="negatives", required=False, action="append", default=[],
            help="Image files that have no annotations (can use glob syntax)")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        return {"inputs": namespace.inputs,
                "negatives": namespace.negatives}
