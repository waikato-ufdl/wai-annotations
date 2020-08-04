from typing import Type, Set

from ...core.component import InlineStreamProcessor
from ...core.specifier import ISPSpecifier
from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier


class FilterLabelsISPSpecifier(ISPSpecifier):
    """
    Specifies the filter-labels ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Filters detected objects down to those with specified labels."

    @classmethod
    def domains(cls) -> Set[Type[ImageObjectDetectionDomainSpecifier]]:
        return {ImageObjectDetectionDomainSpecifier}

    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        from ..filter_labels import FilterLabels
        return FilterLabels
