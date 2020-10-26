from typing import Type, Tuple

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import SinkStageSpecifier


class TFRecordsOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing the binary TFRecords
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image object-detection annotations in the TFRecords binary format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ....core.component.util import Enumerator
        from ..component import ToTensorflowExample, TensorflowExampleWriter
        return ToTensorflowExample, Enumerator, TensorflowExampleWriter

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
