from abc import ABC

from wai.common.cli import CLIInstantiable

from ..logging import LoggingEnabled


class Component(
    LoggingEnabled,
    CLIInstantiable,
    ABC
):
    """

    """
    pass
