from typing import Dict, Type

from ..specifier import StageSpecifier
from ._get_all_plugin_names import get_all_plugin_names
from ._get_plugin_specifier import get_plugin_specifier


def get_all_plugins() -> Dict[str, Type[StageSpecifier]]:
    """
    Gets all plugin specifiers registered with the system.
    """
    return {
        name: get_plugin_specifier(name)
        for name in get_all_plugin_names()
    }
