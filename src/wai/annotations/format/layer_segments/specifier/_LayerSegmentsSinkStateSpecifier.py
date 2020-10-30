from typing import Tuple, Type

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SinkStageSpecifier


class LayerSegmentsSinkStageSpecifier(SinkStageSpecifier):
    """
    Specifies the writing components of the layer-segments format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes the layer-segments image-segmentation format to disk"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import ToLayerSegments, LayerSegmentsWriter
        return ToLayerSegments, LayerSegmentsWriter
