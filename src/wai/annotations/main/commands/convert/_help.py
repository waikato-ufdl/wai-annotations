"""
Provides the help information for the 'convert' sub-command.
"""
from ....core.help import MainUsageFormatter
from ._ConvertOptions import ConvertOptions


def convert_help() -> str:
    """
    Gets the help text for the 'convert' sub-command.
    """
    return ConvertOptions.get_configured_parser(
                prog="wai-annotations convert",
                formatter_class=MainUsageFormatter
            ).format_help()
