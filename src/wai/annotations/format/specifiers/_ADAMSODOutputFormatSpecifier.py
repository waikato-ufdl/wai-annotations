from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class ADAMSODOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing the ADAMS report-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image object-detection annotations in the ADAMS report-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..adams.od.convert import ToADAMSReport
        return ToADAMSReport

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..adams.base.io import ADAMSBaseWriter
        return ADAMSBaseWriter
