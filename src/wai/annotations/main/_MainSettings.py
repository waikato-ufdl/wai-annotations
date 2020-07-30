from argparse import ArgumentParser
from logging import WARNING, INFO, DEBUG

from wai.common.cli import CLIInstantiable
from wai.common.cli.options import CountOption, FlagOption, TypedOption
from wai.common.cli.util import TranslationTable


class MainSettings(CLIInstantiable):
    """
    The main settings class for the library. Contains global
    settings.
    """
    # The verbosity of logging to implement
    VERBOSITY = CountOption(
        "-v",
        translation=TranslationTable(WARNING, INFO, DEBUG),
        help="whether to be more verbose when generating the records"
    )

    # Lists the available plugins and exits
    LIST_PLUGINS = FlagOption(
        "--list-plugins",
        help="lists the available plugins and exits"
    )

    # Provides usage information for the installed plugins
    HELP_PLUGINS = TypedOption(
        "--help-plugins",
        type=str,
        nargs="*",
        default=None,
        help="provides usage information about plugins and exits",
        metavar="PLUGIN"
    )

    # Whether to perform conversions in debug mode
    DEBUG = FlagOption(
        "--debug",
        help="whether to perform conversions in debug mode"
    )

    # Override the default help option
    HELP = FlagOption(
        "-h", "--help",
        help="prints this help message and exits"
    )

    # Lets the user define a macro file other than the default one
    MACRO_FILE = TypedOption(
        "--macro-file",
        type=str,
        default="",
        help="the file to load macros from",
        metavar="FILENAME"
    )

    @classmethod
    def get_configured_parser(self, *, add_help=False, **kwargs) -> ArgumentParser:
        return super().get_configured_parser(add_help=add_help, **kwargs)