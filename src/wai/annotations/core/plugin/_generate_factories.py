"""
Module for tools for generating the factory classes.
"""
from os import mkdir
from os.path import join, exists
from shutil import rmtree
from typing import List, Dict

from wai.common.cli import CLIFactory

from ...core import FormatSpecifier
from .constants import FACTORIES_PACKAGE_DIRECTORY, HEADER
from ._util import factory_name


def clean_factories():
    """
    Cleans the factories package for regeneration.
    """
    # Remove the factories package if it exists
    if exists(FACTORIES_PACKAGE_DIRECTORY):
        # Delete the directory
        rmtree(FACTORIES_PACKAGE_DIRECTORY)

    # Recreate the package
    mkdir(FACTORIES_PACKAGE_DIRECTORY)

    # Create the base __init__.py file
    with open(join(FACTORIES_PACKAGE_DIRECTORY, "__init__.py"), "w") as file:
        file.write(HEADER)


def generate_factories(**format_specifiers: FormatSpecifier) -> Dict[str, List[str]]:
    """
    Generates the cli package from the given components.

    :param components:  The components to make available.
    """
    # Initialise the return value
    generated_factories = {}

    # Process each group
    for format_name, format_specifier in format_specifiers.items():
        # Add the group to the return value
        generated_factories[format_name] = []

        # Write the init file group header
        init_file = join(FACTORIES_PACKAGE_DIRECTORY, "__init__.py")
        with open(init_file, "a") as file:
            file.write(f"\n# Format: {format_name.upper()}\n")

        # Process each component in the group
        for component in format_specifier:
            # Skip missing components
            if component is None:
                generated_factories[format_name].append("")
                continue

            # Get the component's factory name
            fact_name = factory_name(component)

            # Add the factory name to the return value
            generated_factories[format_name].append(fact_name)

            # Write the factory class
            with open(join(FACTORIES_PACKAGE_DIRECTORY, f"_{fact_name}.py"), "w") as file:
                file.write(HEADER)
                file.write(CLIFactory.code_for_class(component))

            # Write the __init__.py file import
            with open(init_file, "a") as file:
                file.write(f"from ._{fact_name} import {fact_name}\n")

    return generated_factories
