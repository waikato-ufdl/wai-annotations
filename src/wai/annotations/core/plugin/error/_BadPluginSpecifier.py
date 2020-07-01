from typing import Type

from pkg_resources import EntryPoint

from ...specifier import PluginSpecifier
from ..constants import PLUGINS_ENTRY_POINT_GROUP


class BadPluginSpecifier(Exception):
    """
    Error for when a plugin-specifier entry-point is incorrectly configured.
    """
    def __init__(self):
        super().__init__(f"Entry points in the '{PLUGINS_ENTRY_POINT_GROUP}' group should "
                         f"be sub-classes of {PluginSpecifier.__qualname__}")

    @staticmethod
    def load_from_entry_point(entry_point: EntryPoint) -> Type[PluginSpecifier]:
        """
        Loads a plugin-specifier from an entry-point, or raises
        an instance of this error if it can't.

        :param entry_point:     The entry-point to load from.
        :return:                The plugin specifier.
        """
        # Make sure all escaping exceptions are of this type
        try:
            # Load the plugin specifier from the entry-point
            format_specifier = entry_point.load()

            # Make sure it is a plugin specifier
            if not issubclass(format_specifier, PluginSpecifier):
                raise BadPluginSpecifier()

            return format_specifier

        # If we raised an instance, let it escape
        except BadPluginSpecifier:
            raise

        # Wrap any other error as an instance
        except Exception as e:
            raise BadPluginSpecifier() from e
