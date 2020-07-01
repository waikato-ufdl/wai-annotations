from typing import Type, Set

from ...core.component import InlineStreamProcessor
from ...core.specifier import ISPSpecifier, DomainSpecifier


class BoxBoundsCoercionISPSpecifier(ISPSpecifier):
    """
    Specifies the box-bounds coercion.
    """
    @classmethod
    def description(cls) -> str:
        return "Converts all annotation bounds into box regions"

    @classmethod
    def domains(cls) -> Set[Type[DomainSpecifier]]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return {ImageObjectDetectionDomainSpecifier}

    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        from ..coercions import BoxBoundsCoercion
        return BoxBoundsCoercion
