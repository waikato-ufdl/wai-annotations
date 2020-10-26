from typing import TypeVar

from ..specifier import StageSpecifier

# A generic plugin-specifier type
PluginSpecifierType = TypeVar("PluginSpecifierType", bound=StageSpecifier)
