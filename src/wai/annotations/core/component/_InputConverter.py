from abc import ABC
from typing import TypeVar

from wai.common.cli import CLIInstantiable

from ..stream import Converter
from ..instance import Instance

ExternalFormat = TypeVar("ExternalFormat")
InstanceType = TypeVar("InstanceType", bound=Instance)


class InputConverter(CLIInstantiable, Converter[ExternalFormat, InstanceType], ABC):
    """
    Base class for converters from an external format to a domain format.
    """
    pass
