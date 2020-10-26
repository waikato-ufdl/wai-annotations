from typing import Dict, Type

from ..specifier import StageSpecifier


# A cache of loaded specifiers for plugins
__cache: Dict[str, Type[StageSpecifier]] = {}


def is_cached(name: str) -> bool:
    """
    Whether a plugin exists in the cache by a given name.

    :param name:    The plugin name.
    :return:        Whether the cache
    """
    return name in __cache


def get_cached(name: str) -> Type[StageSpecifier]:
    """
    Gets a cached plugin specifier.

    :param name:    The name of the plugin to get.
    :return:        The plugin specifier.
    """
    return __cache[name]


def set_cache(name: str, specifier: Type[StageSpecifier]):
    """
    Adds a specifier to the cache.

    :param name:        The name to give the specifier.
    :param specifier:   The specifier.
    """
    __cache[name] = specifier
