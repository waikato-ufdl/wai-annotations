from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SinkStageSpecifier


class SubDirOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing image classification instances where
    each image is stored in a sub-directory named after the class label.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes images to sub-directories named after their class labels."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import SubDirWriter
        return SubDirWriter,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier
