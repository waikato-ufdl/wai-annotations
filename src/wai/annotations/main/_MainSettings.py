from logging import WARNING, INFO, DEBUG

from wai.common.cli import CLIInstantiable
from wai.common.cli.options import CountOption, FlagOption
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
