from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class ADAMSICOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing the ADAMS report-based
    image classification format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image classification annotations in the ADAMS report-format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..adams.ic.convert import ToADAMS
        return ToADAMS

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..adams.base.io import ADAMSBaseWriter
        return ADAMSBaseWriter
