from argparse import ArgumentParser, Namespace
from typing import Type, Dict, Any

from ...core.cli import CommandLineSeparateImageWriterFactory
from ...core import SeparateImageWriter


class CommandLineROIWriterFactory(CommandLineSeparateImageWriterFactory):
    """
    Command-line factory that produces ROIWriter writers.
    """
    @classmethod
    def related_class(cls) -> Type[SeparateImageWriter]:
        from ...roi.io import ROIWriter
        return ROIWriter

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument("--prefix", required=False, dest="prefix",
                            help="the prefix for output filenames (default = '')")

        parser.add_argument("--suffix", required=False, dest="suffix",
                            help="the suffix for output filenames (default = '-rois.csv')")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(prefix=namespace.prefix,
                      suffix=namespace.suffix)
        return kwargs

    @classmethod
    def output_help_text(cls) -> str:
        return "output directory to write files to"
