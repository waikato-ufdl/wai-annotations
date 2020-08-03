from typing import Type

from ...core.component import LocalReader, InputConverter
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class SubDirInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading image classification instances where
    each image is stored in a sub-directory named after the class label.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads images from sub-directories named after their class labels."

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..subdir.io import SubDirReader
        return SubDirReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..subdir.convert import FromSubDir
        return FromSubDir
