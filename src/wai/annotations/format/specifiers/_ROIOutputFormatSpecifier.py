from typing import Type

from ...core.component import OutputConverter, LocalWriter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class ROIOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing the ROI CSV-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image object-detection annotations in the ROI CSV-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..roi.convert import ToROI
        return ToROI

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..roi.io import ROIWriter
        return ROIWriter
