from abc import ABC
from typing import TypeVar

from wai.common.cli import CLIInstantiable

from ..stream import Converter
from ..instance import Instance

ExternalFormat = TypeVar("ExternalFormat")
InstanceType = TypeVar("InstanceType", bound=Instance)


class OutputConverter(CLIInstantiable, Converter[InstanceType, ExternalFormat], ABC):
    """
    Base class for converters from domain-specific instances to an external format.
    """
    pass
