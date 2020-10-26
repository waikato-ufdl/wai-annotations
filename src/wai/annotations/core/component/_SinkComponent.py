from abc import ABC

from ..stream import StreamSink, ElementType
from ._Component import Component


class SinkComponent(
    StreamSink[ElementType],
    Component,
    ABC
):
    """
    Base class for classes which can write a specific external format.
    """
    pass
