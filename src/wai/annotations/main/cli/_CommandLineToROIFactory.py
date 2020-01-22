from argparse import ArgumentParser, Namespace
from typing import Type, Dict, Any

from ...core.cli import CommandLineInternalFormatConverterFactory
from ...core import InternalFormatConverter


class CommandLineToROIFactory(CommandLineInternalFormatConverterFactory):
    """
    Command-line factory that produces ToROI converters.
    """
    @classmethod
    def related_class(cls) -> Type[InternalFormatConverter]:
        from ...roi.convert import ToROI
        return ToROI

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument(
            "-d", "--image-dimensions", metavar="width,height", dest="image_size", required=False,
            help="image dimensions to use if none can be inferred",
            default="")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(
            image_size=tuple(map(int, namespace.image_size.split(","))) if len(namespace.image_size) > 0 else None
        )
        return kwargs
