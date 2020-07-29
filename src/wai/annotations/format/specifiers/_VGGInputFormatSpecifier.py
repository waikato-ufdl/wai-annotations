from typing import Type

from ...core.component import InputConverter, LocalReader
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class VGGInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading the VGG JSON-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image object-detection annotations in the VGG JSON-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..vgg.io import VGGReader
        return VGGReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..vgg.convert import FromVGG
        return FromVGG
