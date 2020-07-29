from typing import Type

from ...core.component import LocalReader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class COCOInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading the MS-COCO JSON-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image object-detection annotations in the MS-COCO JSON-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..coco.io import COCOReader
        return COCOReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..coco.convert import FromCOCO
        return FromCOCO
