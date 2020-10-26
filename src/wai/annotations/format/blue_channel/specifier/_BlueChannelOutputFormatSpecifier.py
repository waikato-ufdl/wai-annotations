from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SinkStageSpecifier


class BlueChannelOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing blue-channel format
    image-segmentation annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image segmentation files in the blue-channel format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import ToBlueChannel, BlueChannelWriter
        return ToBlueChannel, BlueChannelWriter

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier
