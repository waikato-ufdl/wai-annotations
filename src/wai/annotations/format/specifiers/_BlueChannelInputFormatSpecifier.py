from typing import Type

from ...core.component import LocalReader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class BlueChannelInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading blue-channel format
    image-segmentation annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image segmentation files in the blue-channel format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..blue_channel.io import BlueChannelReader
        return BlueChannelReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..blue_channel.convert import FromBlueChannel
        return FromBlueChannel
