from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class COCOOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing the MS-COCO JSON-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image object-detection annotations in the MS-COCO JSON-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..coco.convert import ToCOCO
        return ToCOCO

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..coco.io import COCOWriter
        return COCOWriter
