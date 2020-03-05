from argparse import ArgumentParser, Namespace
from typing import Type, Dict, Any

from ...core.cli import CommandLineSeparateImageWriterFactory
from ...core import SeparateImageWriter


class CommandLineVGGWriterFactory(CommandLineSeparateImageWriterFactory):
    """
    Command-line factory that produces VGGWriter writers.
    """
    @classmethod
    def related_class(cls) -> Type[SeparateImageWriter]:
        from ...vgg.io import VGGWriter
        return VGGWriter

    @classmethod
    def output_help_text(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"

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
