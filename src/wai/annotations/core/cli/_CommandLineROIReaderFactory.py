from argparse import ArgumentParser, Namespace
from typing import Type, Dict, Any

from ...core.cli import CommandLineReaderFactory
from ...core import Reader


class CommandLineROIReaderFactory(CommandLineReaderFactory):
    """
    Command-line factory that produces ROIReader readers.
    """
    @classmethod
    def related_class(cls) -> Type[Reader]:
        from ...roi.io import ROIReader
        return ROIReader

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument("--prefix", required=False, dest="roi_reader_prefix",
                            help="the prefix for output filenames (default = '')")

        parser.add_argument("--suffix", required=False, dest="roi_writer_suffix",
                            help="the suffix for output filenames (default = '-rois.csv')")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(prefix=namespace.roi_reader_prefix,
                      suffix=namespace.roi_writer_suffix)
        return kwargs
