from typing import Type

from ...core.component import LocalReader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class IndexedPNGInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading indexed-PNG format
    image-segmentation annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image segmentation files in the indexed-PNG format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..indexed_png.io import IndexedPNGReader
        return IndexedPNGReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..indexed_png.convert import FromIndexedPNG
        return FromIndexedPNG
