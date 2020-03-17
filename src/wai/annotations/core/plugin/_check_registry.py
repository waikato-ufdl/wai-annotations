from os.path import join
from pkg_resources import working_set, EntryPoint
from typing import Tuple

from wai.common.meta.code_repr import code_repr, get_import_dict, get_code

from .constants import FORMATS_ENTRY_POINT_GROUP, HEADER, PLUGIN_PACKAGE_DIRECTORY
from .error import BadFormatSpecifier
from .registry import PluginRegistry
from ._generate_factories import generate_factories, clean_factories


def check_registry():
    """
    Checks to see if the registry of known plugins has changed,
    and auto-generates the required factory classes for them if
    it has.
    """
    # Get the entry-points defined in the working-set
    entry_points: Tuple[EntryPoint, ...] = tuple(working_set.iter_entry_points(FORMATS_ENTRY_POINT_GROUP))

    # Get a light-weight version of the registry to see if it's changed
    registry: PluginRegistry = PluginRegistry.from_entry_points(entry_points)

    # Check if we need to rebuild the registry
    try:
        from ._registry import registry as current_registry
        requires_rebuild = current_registry != registry
    except Exception:
        requires_rebuild = True

    # Rebuild the registry if needed
    if requires_rebuild:
        # Regenerate the factory classes
        clean_factories()
        generated_factories = generate_factories(
            **{entry_point.name: BadFormatSpecifier.load_from_entry_point(entry_point)
               for entry_point in entry_points}
        )

        # Update the registry with the factories
        for format_name, factories in generated_factories.items():
            registry[format_name].set_components(*factories)

        # Write the registry
        registry_code_repr = code_repr(registry)

        with open(join(PLUGIN_PACKAGE_DIRECTORY, "_registry.py"), "w") as file:
            file.write(HEADER)
            for import_code in get_import_dict(registry_code_repr).values():
                file.write(import_code + "\n")
            file.write("\n")
            file.write("registry = " + get_code(registry_code_repr) + "\n")

        # As the registry has changed, the module will need reloading
        # (if we could load it initially)
        import sys
        registry_package = f"{__package__}._registry"
        if registry_package in sys.modules:
            del sys.modules[registry_package]
