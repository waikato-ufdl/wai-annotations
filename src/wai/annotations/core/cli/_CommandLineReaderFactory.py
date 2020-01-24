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
            "-i", "--inputs", metavar="files", dest="inputs", required=False, action="append", default=[],
            help="Input annotations files (can use glob syntax)")
        parser.add_argument(
            "-n", "--negatives", metavar="image", dest="negatives", required=False, action="append", default=[],
            help="Image files that have no annotations (can use glob syntax)")
        parser.add_argument(
            "-I", "--input-files", dest="input_files", required=False, action="append", default=[],
            help="Files containing lists of input annotation files (can use glob syntax)")
        parser.add_argument(
            "-N", "--negative-files", dest="negative_files", required=False, action="append", default=[],
            help="Files containing lists of negative images (can use glob syntax)")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        return {"inputs": namespace.inputs,
                "negatives": namespace.negatives,
                "input_files": namespace.input_files,
                "negative_files": namespace.negative_files}
