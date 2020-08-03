from typing import Type, Set

from ...core.component import InlineStreamProcessor
from ...core.specifier import ISPSpecifier
from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier


class MapLabelsISPSpecifier(ISPSpecifier):
    """
    Specifies the map-labels ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Maps object-detection labels from one set to another"

    @classmethod
    def domains(cls) -> Set[Type[ImageObjectDetectionDomainSpecifier]]:
        return {ImageObjectDetectionDomainSpecifier}

    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        from ..map_labels import MapLabels
        return MapLabels
