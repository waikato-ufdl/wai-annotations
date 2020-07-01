from typing import Type, Set

from ...core.component import InlineStreamProcessor
from ...core.specifier import ISPSpecifier, DomainSpecifier


class DimensionDiscarderISPSpecifier(ISPSpecifier):
    """
    Specifies the dimension-discarder.
    """
    @classmethod
    def description(cls) -> str:
        return "Removes annotations which fall outside certain size constraints"

    @classmethod
    def domains(cls) -> Set[Type[DomainSpecifier]]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return {ImageObjectDetectionDomainSpecifier}

    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        from ..dimension_discarder import DimensionDiscarder
        return DimensionDiscarder
