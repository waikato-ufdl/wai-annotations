from typing import Type

from ...specifier import StageSpecifier
from ...specifier.util import specifier_type_string


class BadPluginType(Exception):
    """
    Exception for when a plugin is requested for the wrong type.
    """
    def __init__(self, name: str, required_type: Type[StageSpecifier], actual_type: Type[StageSpecifier]):
        super().__init__(f"Attempted to use plugin '{name}' as a plugin of type '{specifier_type_string(required_type)}'; "
                         f"it is actually of type '{specifier_type_string(actual_type)}'")

