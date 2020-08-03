from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class SubDirOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing image classification instances where
    each image is stored in a sub-directory named after the class label.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes images to sub-directories named after their class labels."

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.classification import ImageClassificationDomainSpecifier
        return ImageClassificationDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..subdir.convert import ToSubDir
        return ToSubDir

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..subdir.io import SubDirWriter
        return SubDirWriter
