from argparse import ArgumentParser, Namespace
from typing import Type, Dict, Any

from ...core.cli import CommandLineSeparateImageWriterFactory
from ...core import SeparateImageWriter


class CommandLineCOCOWriterFactory(CommandLineSeparateImageWriterFactory):
    """
    Command-line factory that produces COCOWriter writers.
    """
    @classmethod
    def related_class(cls) -> Type[SeparateImageWriter]:
        from ...coco.io import COCOWriter
        return COCOWriter

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument("--license-name", required=False, dest="license_name", default="",
                            help="the license of the images")

        parser.add_argument("--license-url", required=False, dest="license_url", default="",
                            help="the license of the images")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(license_name=namespace.license_name,
                      license_url=namespace.license_url)
        return kwargs

    @classmethod
    def output_help_text(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"
