from typing import Type

from ...core.component import LocalReader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class ROIInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading the ROI CSV-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image object-detection annotations in the ROI CSV-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..roi.io import ROIReader
        return ROIReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..roi.convert import FromROI
        return FromROI
