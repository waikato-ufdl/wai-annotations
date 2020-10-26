from ..specifier.util import specifier_type
from ._cache import *
from ._get_all_plugins import get_all_plugins


def get_all_plugins_by_type() -> Dict[Type[StageSpecifier], Dict[str, Type[StageSpecifier]]]:
    """
    Gets a dictionary from plugin base-type to the plugins
    of that type registered with the system.
    """
    # Create the empty result object
    all_plugins_by_type: Dict[Type[StageSpecifier], Dict[str, Type[StageSpecifier]]] = {}

    # Add each plugin to a set under its base-type
    for name, plugin_specifier in get_all_plugins().items():
        # Get the base-type of the plugin
        base_type = specifier_type(plugin_specifier)

        # Create a new group for this base-type if none exists already
        if base_type not in all_plugins_by_type:
            all_plugins_by_type[base_type] = {}

        # Add this plugin to its base-type group
        all_plugins_by_type[base_type][name] = plugin_specifier

    return all_plugins_by_type
