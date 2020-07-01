from typing import Type

from ...specifier import PluginSpecifier


class BadPluginType(Exception):
    """
    Exception for when a plugin is requested for the wrong type.
    """
    def __init__(self, name: str, required_type: Type[PluginSpecifier], actual_type: Type[PluginSpecifier]):
        super().__init__(f"Attempted to use plugin '{name}' as a plugin of type '{required_type.type_string()}'; "
                         f"it is actually of type '{actual_type.type_string()}'")

