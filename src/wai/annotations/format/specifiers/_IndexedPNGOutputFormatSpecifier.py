from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class IndexedPNGOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing indexed-PNG format
    image-segmentation annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image segmentation files in the indexed-PNG format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..indexed_png.convert import ToIndexedPNG
        return ToIndexedPNG

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..indexed_png.io import IndexedPNGWriter
        return IndexedPNGWriter
