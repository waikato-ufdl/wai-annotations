"""
Constants related to the plugin system.
"""
from os.path import dirname as _dirname, join as _join

# The entry-point group used for registering formats
FORMATS_ENTRY_POINT_GROUP = "wai.annotations.formats"

# The header to write at the beginning of each generated file
HEADER = (
    '"""\n'
    'Automatically generated.\n'
    '"""\n'
)

# The base directory of the plugin package
PLUGIN_PACKAGE_DIRECTORY = _dirname(__file__)

# The directory for keeping factories
FACTORIES_PACKAGE_DIRECTORY = _join(PLUGIN_PACKAGE_DIRECTORY, "factories")

# The directory for keeping the registry
REGISTRY_PACKAGE_DIRECTORY = _join(PLUGIN_PACKAGE_DIRECTORY, "registry")
