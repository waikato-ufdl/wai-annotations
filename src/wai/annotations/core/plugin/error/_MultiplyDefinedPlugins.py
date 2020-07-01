from typing import List

from pkg_resources import EntryPoint


class MultiplyDefinedPlugins(Exception):
    """
    Exception for when a plugin name is defined more than once.
    """
    def __init__(self, **definitions: List[EntryPoint]):
        super().__init__("Some plugins are multiply-defined:\n" +
                         "\n".join(
                             f"{name}: {format_definitions}"
                             for name, format_definitions in definitions
                         ))

    @staticmethod
    def check_entry_points(*entry_points: EntryPoint):
        """
        Checks that no plugin name is multiply-defined.

        :param entry_points:    The entry-points to check.
        """
        # Create a dictionary from plugin name to its definitions
        definitions = {}

        # Process all of the entry-points
        for entry_point in entry_points:
            if entry_point.name not in definitions:
                definitions[entry_point.name] = []
            definitions[entry_point.name].append(entry_point)

        # Remove any plugin names that are only defined once (the correct amount)
        correctly_defined = []
        for format_name, format_definitions in definitions.items():
            if len(format_definitions) == 1:
                correctly_defined.append(format_name)
        for format_name in correctly_defined:
            definitions.pop(format_name)

        # If there are any definitions left, raise
        if len(definitions) > 0:
            raise MultiplyDefinedPlugins(**definitions)
