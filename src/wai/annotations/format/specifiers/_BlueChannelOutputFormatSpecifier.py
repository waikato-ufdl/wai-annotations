from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class BlueChannelOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing blue-channel format
    image-segmentation annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image segmentation files in the blue-channel format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..blue_channel.convert import ToBlueChannel
        return ToBlueChannel

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..blue_channel.io import BlueChannelWriter
        return BlueChannelWriter
