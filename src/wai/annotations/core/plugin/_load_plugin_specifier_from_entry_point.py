from typing import Type

from pkg_resources import EntryPoint

from ..specifier import StageSpecifier
from ..specifier.util import validate_stage_specifier
from .error import BadPluginSpecifier


def load_plugin_specifier_from_entry_point(entry_point: EntryPoint) -> Type[StageSpecifier]:
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
        if not issubclass(format_specifier, StageSpecifier):
            raise BadPluginSpecifier()

        # Validate the specifier
        validate_stage_specifier(format_specifier)

        return format_specifier

    # If we raised an instance, let it escape
    except BadPluginSpecifier:
        raise

    # Wrap any other error as an instance
    except Exception as e:
        raise BadPluginSpecifier() from e
