from abc import ABC
from typing import TypeVar

from wai.common.cli import CLIInstantiable

from ..stream import InlineStreamProcessor as BasicInlineStreamProcessor
from ..instance import Instance

InstanceType = TypeVar("InstanceType", bound=Instance)


class InlineStreamProcessor(CLIInstantiable, BasicInlineStreamProcessor[InstanceType], ABC):
    """
    Base class for plugin ISPs.
    """
    pass
