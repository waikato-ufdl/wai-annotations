from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class VGGOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing the VGG JSON-based
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image object-detection annotations in the VGG JSON-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..vgg.convert import ToVGG
        return ToVGG

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..vgg.io import VGGWriter
        return VGGWriter