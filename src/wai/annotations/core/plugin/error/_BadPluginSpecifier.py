from typing import Type

from pkg_resources import EntryPoint

from ...specifier import StageSpecifier
from ...specifier.util import validate_stage_specifier
from ..constants import PLUGINS_ENTRY_POINT_GROUP


class BadPluginSpecifier(Exception):
    """
    Error for when a plugin-specifier entry-point is incorrectly configured.
    """
    def __init__(self):
        super().__init__(f"Entry points in the '{PLUGINS_ENTRY_POINT_GROUP}' group should "
                         f"be sub-classes of {StageSpecifier.__qualname__}")
