from typing import Tuple, Type

from pkg_resources import EntryPoint

from ..specifier import *
from .error import *
from ._cache import is_cached, get_cached, set_cache
from ._load_plugin_specifier_from_entry_point import load_plugin_specifier_from_entry_point
from ._plugin_entry_points import plugin_entry_points


def get_plugin_specifier(name: str) -> Type[StageSpecifier]:
    """
    Gets the plugin specifier for the given name.

    :param name:    The name of the specifier.
    :return:        The specifier.
    """
    # Check the cache
    if is_cached(name):
        return get_cached(name)

    # Get the plugin entry-points for the given name
    entry_points: Tuple[EntryPoint] = tuple(plugin_entry_points(name))

    # Make sure there is one and only one entry-point for the name
    if len(entry_points) > 1:
        # If this name is multiply-defined, perhaps others are too?
        MultiplyDefinedPlugins.check_entry_points(*plugin_entry_points())
    elif len(entry_points) == 0:
        raise UnknownPluginName(name)

    # Get the plugin entry-point
    plugin_entry_point: EntryPoint = entry_points[0]

    # Load the plugin specifier
    plugin_specifier = load_plugin_specifier_from_entry_point(plugin_entry_point)

    # Make sure it's of a known type,
    if not issubclass(plugin_specifier, (SourceStageSpecifier, SinkStageSpecifier, ProcessorStageSpecifier)):
        # TODO: Better error type
        raise BadPluginType(name, StageSpecifier, plugin_specifier)

    # Cache it
    set_cache(name, plugin_specifier)

    return plugin_specifier
