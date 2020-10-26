from abc import ABC
from typing import TypeVar, Type

from ...core.domain import Instance
from ._Image import Image

AnnotationsType = TypeVar("AnnotationsType")


class ImageInstance(Instance[Image, AnnotationsType], ABC):
    """
    Base class for instances in image-based domains.
    """
    @classmethod
    def data_type(cls) -> Type[Image]:
        return Image
