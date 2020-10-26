from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SinkStageSpecifier


class ROIOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing the ROI CSV-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image object-detection annotations in the ROI CSV-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import ToROI, ROIWriter
        return ToROI, ROIWriter

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
