from typing import Type, Set

from ...core.component import InlineStreamProcessor
from ...core.specifier import ISPSpecifier, DomainSpecifier


class MaskBoundsCoercionISPSpecifier(ISPSpecifier):
    """
    Specifies the mask-bounds coercion.
    """
    @classmethod
    def description(cls) -> str:
        return "Converts all annotation bounds into polygon regions"

    @classmethod
    def domains(cls) -> Set[Type[DomainSpecifier]]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return {ImageObjectDetectionDomainSpecifier}

    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        from ..coercions import MaskBoundsCoercion
        return MaskBoundsCoercion
