"""
Provides the help information for the 'plugins' sub-command.
"""
from ._PluginsOptions import PluginsOptions


def plugins_help() -> str:
    """
    Gets the help text for the 'plugins' sub-command.
    """
    return PluginsOptions.get_configured_parser(prog="wai-annotations plugins").format_help()
