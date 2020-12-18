from argparse import ArgumentParser
from logging import WARNING, INFO, DEBUG

from wai.common.cli import CLIInstantiable
from wai.common.cli.options import CountOption, FlagOption, TypedOption
from wai.common.cli.util import TranslationTable


class ConvertOptions(CLIInstantiable):
    """
    The global options for a conversion.
    """
    # The verbosity of logging to implement
    VERBOSITY = CountOption(
        "-v",
        translation=TranslationTable(WARNING, INFO, DEBUG),
        help="whether to be more verbose when generating the records"
    )

    # Lets the user define a macro file other than the default one
    MACRO_FILE = TypedOption(
        "--macro-file",
        type=str,
        default="",
        help="the file to load macros from",
        metavar="FILENAME"
    )

    # Override the default help option
    HELP = FlagOption(
        "-h", "--help",
        help="prints this help message and exits"
    )

    @classmethod
    def get_configured_parser(cls, *, add_help=False, **kwargs) -> ArgumentParser:
        return super().get_configured_parser(add_help=add_help, **kwargs)
