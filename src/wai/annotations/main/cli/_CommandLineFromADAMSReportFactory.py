from argparse import ArgumentParser, Namespace
from typing import Type, Dict, Any

from ...core.cli import CommandLineExternalFormatConverterFactory
from ...core import ExternalFormatConverter


class CommandLineFromADAMSReportFactory(CommandLineExternalFormatConverterFactory):
    """
    Command-line factory that produces FromADAMSReport converters.
    """
    @classmethod
    def related_class(cls) -> Type[ExternalFormatConverter]:
        from ...adams.convert import FromADAMSReport
        return FromADAMSReport

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument(
            "-p", "--prefixes", metavar="prefix1,prefix2,...", dest="prefixes", required=False,
            help="comma-separated list of prefixes to parse", default="")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(prefixes=list(namespace.prefixes.split(",")) if len(namespace.prefixes) > 0 else None)
        return kwargs
