"""
Module for utility functions for the plugin system.
"""
from typing import Type

from wai.common.cli import CLIInstantiable


def factory_name(component: Type[CLIInstantiable]) -> str:
    """
    Gets the factory name used for a given component.

    :param component:   The component.
    :return:            The component's factory name.
    """
    return f"{component.__name__}CLIFactory"
