from typing import Type

from ...core.component import Reader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class ADAMSInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading the ADAMS report-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image object-detection annotations in the ADAMS report-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def reader(cls) -> Type[Reader]:
        from ..adams.io import ADAMSReportReader
        return ADAMSReportReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..adams.convert import FromADAMSReport
        return FromADAMSReport
