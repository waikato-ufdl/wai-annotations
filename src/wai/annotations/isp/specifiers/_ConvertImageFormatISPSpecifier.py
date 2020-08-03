from typing import Type, Set

from ...core.component import InlineStreamProcessor
from ...core.specifier import ISPSpecifier, DomainSpecifier
from ...domain.image.classification import ImageClassificationDomainSpecifier
from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier


class ConvertImageFormatISPSpecifier(ISPSpecifier):
    """
    Specifies the convert-image-format ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Converts images from one format to another"

    @classmethod
    def domains(cls) -> Set[Type[DomainSpecifier]]:
        return {ImageObjectDetectionDomainSpecifier,
                ImageClassificationDomainSpecifier}

    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        from ..convert_image_format import ConvertImageFormat
        return ConvertImageFormat
