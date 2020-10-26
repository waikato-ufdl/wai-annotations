from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SourceStageSpecifier


class SubDirInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading image classification instances where
    each image is stored in a sub-directory named after the class label.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads images from sub-directories named after their class labels."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ....core.component.util import LocalFilenameSource
        from ..component import SubDirReader
        return LocalFilenameSource, SubDirReader

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier
