from abc import ABC
from typing import TypeVar, Type

from ...core.domain import Instance
from ._Audio import Audio

AnnotationsType = TypeVar("AnnotationsType")


class AudioInstance(Instance[Audio, AnnotationsType], ABC):
    """
    Base class for instances in audio domains.
    """
    @classmethod
    def data_type(cls) -> Type[Audio]:
        return Audio
