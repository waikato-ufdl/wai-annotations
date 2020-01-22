from abc import ABC
from argparse import ArgumentParser, Namespace
from typing import Dict, Any

from .._ExternalFormatConverter import ExternalFormatConverter
from ._CommandLineConverterFactory import CommandLineConverterFactory


class CommandLineExternalFormatConverterFactory(CommandLineConverterFactory[ExternalFormatConverter], ABC):
    """
    Base class for command-line factories that produce external-format converters.
    """
    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument(
            "-m", "--mapping", metavar="old=new", dest="mapping", action='append', type=str, required=False,
            help="mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)",
            default=list())

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        # Create the empty mapping
        mapping = {}

        # Add each provided exchange to the mapping
        for map_string in namespace.mapping:
            old, new = map_string.split("=")

            # Make sure we don't double-map a label
            if old in mapping:
                raise ValueError(f"Multiple mappings specified for label '{old}': "
                                 f"{mapping[old]}, {new}")

            mapping[old] = new

        return {"label_mapping": mapping}
