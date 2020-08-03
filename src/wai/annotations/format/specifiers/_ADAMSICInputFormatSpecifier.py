from typing import Type

from ...core.component import LocalReader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class ADAMSICInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading the ADAMS report-based
    image classification format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image classification annotations in the ADAMS report-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..adams.base.io import ADAMSBaseReader
        return ADAMSBaseReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..adams.ic.convert import FromADAMS
        return FromADAMS
