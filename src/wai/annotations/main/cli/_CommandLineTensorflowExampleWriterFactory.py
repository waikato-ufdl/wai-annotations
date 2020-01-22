from argparse import ArgumentParser, Namespace
from typing import Type, Dict, Any

from ...core.cli import CommandLineWriterFactory
from ...core import Writer


class CommandLineTensorflowExampleWriterFactory(CommandLineWriterFactory):
    """
    Command-line factory that produces TensorflowExampleWriter writers.
    """
    @classmethod
    def related_class(cls) -> Type[Writer]:
        from ...tf.io import TensorflowExampleWriter
        return TensorflowExampleWriter

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument(
            "-s", "--shards", metavar="num", dest="shards", required=False, type=int,
            help="number of shards to split the images into (<= 1 for off)", default=-1)

        parser.add_argument(
            "-p", "--protobuf", metavar="file", dest="protobuf_label_map", required=False,
            help="for storing the label strings and IDs", default=None)

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(shards=namespace.shards,
                      protobuf_label_map=namespace.protobuf_label_map)
        return kwargs

    @classmethod
    def output_help_text(cls) -> str:
        return "name of output file for TFRecords"
