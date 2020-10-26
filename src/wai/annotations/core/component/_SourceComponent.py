from abc import ABC

from ..stream import StreamSource, ElementType
from ._Component import Component


class SourceComponent(
    StreamSource[ElementType],
    Component,
    ABC
):
    """
    Base class for classes which can read a specific external format.
    """
    pass
