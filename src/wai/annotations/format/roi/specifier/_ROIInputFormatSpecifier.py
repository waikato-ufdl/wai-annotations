from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SourceStageSpecifier


class ROIInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading the ROI CSV-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image object-detection annotations in the ROI CSV-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ....core.component.util import LocalFilenameSource
        from ..component import ROIReader, FromROI
        return LocalFilenameSource, ROIReader, FromROI

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
