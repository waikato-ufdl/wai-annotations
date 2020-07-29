from typing import Type

from ...core.component import InputConverter, LocalReader
from ...core.specifier import InputFormatSpecifier, DomainSpecifier


class TFRecordsInputFormatSpecifier(InputFormatSpecifier):
    """
    Specifier of the components for reading the binary TFRecords
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads image object-detection annotations in the TFRecords binary format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def reader(cls) -> Type[LocalReader]:
        from ..tf.io import TensorflowExampleReader
        return TensorflowExampleReader

    @classmethod
    def input_converter(cls) -> Type[InputConverter]:
        from ..tf.convert import FromTensorflowExample
        return FromTensorflowExample
