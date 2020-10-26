from typing import Type, Tuple

from .....core.component import Component
from .....core.domain import DomainSpecifier
from .....core.specifier import SourceStageSpecifier


class ADAMSICInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading the ADAMS report-based
    image classification format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image classification annotations in the ADAMS report-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ...base.component import ADAMSFilenameSource, ADAMSBaseReader
        from ..component import FromADAMS
        return ADAMSFilenameSource, ADAMSBaseReader, FromADAMS

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from .....domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier
