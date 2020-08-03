from typing import Type

from ...core.component import LocalReader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class ADAMSODInputFormatSpecifier(InputFormatSpecifier):
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
    def reader(cls) -> Type[LocalReader]:
        from ..adams.base.io import ADAMSBaseReader
        return ADAMSBaseReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..adams.od.convert import FromADAMSReport
        return FromADAMSReport
