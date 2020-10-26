from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SourceStageSpecifier


class BlueChannelInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading blue-channel format
    image-segmentation annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image segmentation files in the blue-channel format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ....core.component.util import LocalFilenameSource
        from ..component import BlueChannelReader, FromBlueChannel
        return LocalFilenameSource, BlueChannelReader, FromBlueChannel

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier
