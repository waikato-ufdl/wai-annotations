from typing import Type, Tuple

from ....core.component import Component
from ....core.component.util import LocalFilenameSource
from ....core.domain import DomainSpecifier
from ....core.specifier import SourceStageSpecifier


class COCOInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading the MS-COCO JSON-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image object-detection annotations in the MS-COCO JSON-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import FromCOCO
        return LocalFilenameSource, FromCOCO

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
