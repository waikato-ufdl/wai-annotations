from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SourceStageSpecifier


class VGGInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading the VGG JSON-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image object-detection annotations in the VGG JSON-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ....core.component.util import LocalFilenameSource
        from ..component import FromVGG, VGGReader
        return LocalFilenameSource, VGGReader, FromVGG

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
