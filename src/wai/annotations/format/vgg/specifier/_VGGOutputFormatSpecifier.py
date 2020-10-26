from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SinkStageSpecifier


class VGGOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing the VGG JSON-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image object-detection annotations in the VGG JSON-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import ToVGG, VGGWriter
        return ToVGG, VGGWriter

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
