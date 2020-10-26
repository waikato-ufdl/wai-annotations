from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SourceStageSpecifier


class TFRecordsInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading the binary TFRecords
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image object-detection annotations in the TFRecords binary format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ....core.component.util import LocalFilenameSource
        from ..component import TensorflowExampleReader, FromTensorflowExample
        return LocalFilenameSource, TensorflowExampleReader, FromTensorflowExample

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
