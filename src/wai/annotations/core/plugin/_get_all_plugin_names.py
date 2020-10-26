from typing import Set

from ._plugin_entry_points import plugin_entry_points


def get_all_plugin_names() -> Set[str]:
    """
    Gets the set of all plugin names registered with the system.
    """
    return {
        entry_point.name
        for entry_point in plugin_entry_points()
    }
