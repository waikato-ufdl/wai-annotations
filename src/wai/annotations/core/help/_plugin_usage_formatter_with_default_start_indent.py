from typing import Type

from ._PluginUsageFormatter import PluginUsageFormatter


def plugin_usage_formatter_with_default_start_indent(start_indent: int) -> Type[PluginUsageFormatter]:
    """
    Creates a plugin usage-formatter class which has a particular default
    value for the start_indent parameter.

    :param start_indent:    The default value to use.
    :return:                The formatter class.
    """
    # Create a sub-class which overrides the default
    class PluginUsageFormatterWithDefaultStartIndent(PluginUsageFormatter):
        def __init__(self,
                     prog,
                     indent_increment=2,
                     max_help_position=24,
                     width=10000):
            super().__init__(prog,
                             indent_increment=indent_increment,
                             max_help_position=max_help_position,
                             width=width,
                             start_indent=start_indent)

    return PluginUsageFormatterWithDefaultStartIndent
