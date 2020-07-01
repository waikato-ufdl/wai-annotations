from argparse import HelpFormatter


class PluginUsageFormatter(HelpFormatter):
    """
    Helper class for formatting the usage options of plugin components.
    """
    def __init__(self,
                 prog,
                 indent_increment=2,
                 max_help_position=24,
                 width=10000,
                 start_indent=0):
        super().__init__(prog,
                         indent_increment=indent_increment,
                         max_help_position=max_help_position,
                         width=width)

        self._current_indent = start_indent
