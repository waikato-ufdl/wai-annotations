from typing import Tuple, TypeVar, Type, Union, Set, Optional, Iterator, Dict

from pkg_resources import working_set, EntryPoint

from ..specifier import *
from .constants import PLUGINS_ENTRY_POINT_GROUP
from .error import *

# A generic plugin-specifier type
PluginSpecifierType = TypeVar("PluginSpecifierType", bound=PluginSpecifier)

# A cache of loaded specifiers for plugins
__cache: Dict[str, PluginSpecifier] = {}


def get_plugin_specifier(name: str) -> Type[PluginSpecifier]:
    """
    Gets the plugin specifier for the given name.

    :param name:    The name of the specifier.
    :return:        The specifier.
    """
    # Check the cache
    global __cache
    if name in __cache:
        return __cache[name]

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
    specifier = BadPluginSpecifier.load_from_entry_point(plugin_entry_point)

    # Cache it
    __cache[name] = specifier

    return specifier


def get_plugin_specifier_of_type(name: str, type: Type[PluginSpecifierType]) -> Type[PluginSpecifierType]:
    """
    Gets the plugin specifier with the given name, ensuring it is
    of the given type.

    :param name:    The name of the plugin specifier.
    :param type:    The asserted type.
    :return:        The plugin specifier.
    """
    # Get the plugin specifier by name
    plugin_specifier = get_plugin_specifier(name)

    # Make sure it's of the right type
    if not issubclass(plugin_specifier, type):
        raise BadPluginType(name, type, plugin_specifier)

    return plugin_specifier


def get_plugin_specifier_of_known_type(name: str) -> Type[Union[InputFormatSpecifier, OutputFormatSpecifier, ISPSpecifier, XDCSpecifier]]:
    """
    Gets a plugin specifier by name and makes sure it's one of the known
    types of specifier.

    :param name:    The name of the specifier.
    :return:        The specifier.
    """
    # Get the specifier
    plugin_specifier = get_plugin_specifier(name)

    # Make sure it's a known type
    if not issubclass(plugin_specifier, (InputFormatSpecifier, OutputFormatSpecifier, ISPSpecifier, XDCSpecifier)):
        # TODO: Better error type
        raise BadPluginType(name, PluginSpecifier, plugin_specifier)

    return plugin_specifier


def plugin_entry_points(name: Optional[str] = None) -> Iterator[EntryPoint]:
    """
    Iterates through all plugin entry-points with the given name.

    :param name:    The name to search for, or None for all names.
    :return:        An iterator of entry-points.
    """
    return working_set.iter_entry_points(PLUGINS_ENTRY_POINT_GROUP, name)


def get_all_plugin_names() -> Set[str]:
    """
    Gets the set of all plugin names registered with the system.
    """
    return {
        entry_point.name
        for entry_point in plugin_entry_points()
    }


def cache_all():
    """
    Makes sure all plugins have been cached.
    """
    # Getting the specifier for a name caches it
    for name in get_all_plugin_names():
        get_plugin_specifier(name)


def get_all_plugins_of_type(type: Type[PluginSpecifierType]) -> Dict[str, PluginSpecifierType]:
    """
    Gets all plugins of the given specifier type.

    :param type:    The type of plugin to collect.
    :return:        A dictionary of plugin names to their specifiers.
    """
    # Make sure all plugins are loaded
    cache_all()

    global __cache
    return {
        name: specifier
        for name, specifier in __cache.items()
        if issubclass(specifier, type)
    }


def get_all_plugins() -> Dict[str, Type[PluginSpecifier]]:
    """
    Gets all plugin specifiers registered with the system.
    """
    return {name: get_plugin_specifier(name) for name in get_all_plugin_names()}


def get_all_plugins_by_type() -> Dict[str, Dict[str, Type[PluginSpecifier]]]:
    """
    Gets a dictionary from plugin type-string to the plugins
    of that type registered with the system.
    """
    # Create the empty result object
    all_plugins_by_type: Dict[str, Dict[str, Type[PluginSpecifier]]] = {}

    # Add each plugin to a set under its type-string
    for name, plugin_specifier in get_all_plugins().items():
        if plugin_specifier.type_string() not in all_plugins_by_type:
            all_plugins_by_type[plugin_specifier.type_string()] = {}
        all_plugins_by_type[plugin_specifier.type_string()][name] = plugin_specifier

    return all_plugins_by_type
