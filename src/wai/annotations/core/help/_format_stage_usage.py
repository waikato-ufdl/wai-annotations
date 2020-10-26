from typing import Type

from ..specifier import StageSpecifier
from ..specifier.util import get_configured_stage_parser
from ._plugin_usage_formatter_with_default_start_indent import plugin_usage_formatter_with_default_start_indent


def format_stage_usage(specifier: Type[StageSpecifier], name: str, indent: int = 0) -> str:
    """
    Formats the usage text for a plugin stage.

    :param specifier:   The stage specifier
    :param name:        The name the plugin is registered under in the plugin system.
    :param indent:      The indentation level of the text.
    :return:            The usage text.
    """
    return (" " * indent) + get_configured_stage_parser(
        specifier,
        prog=name,
        add_help=False,
        formatter_class=plugin_usage_formatter_with_default_start_indent(indent)
    ).format_help()
