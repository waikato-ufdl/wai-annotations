from abc import ABC

from ..stream import StreamProcessor, InputElementType, OutputElementType
from ._Component import Component


class ProcessorComponent(
    StreamProcessor[InputElementType, OutputElementType],
    Component,
    ABC
):
    """
    Base class for plugin ISPs.
    """
    pass
