from typing import Optional, Iterator

from pkg_resources import working_set, EntryPoint

from .constants import PLUGINS_ENTRY_POINT_GROUP


def plugin_entry_points(name: Optional[str] = None) -> Iterator[EntryPoint]:
    """
    Iterates through all plugin entry-points with the given name.

    :param name:    The name to search for, or None for all names.
    :return:        An iterator of entry-points.
    """
    return working_set.iter_entry_points(PLUGINS_ENTRY_POINT_GROUP, name)
