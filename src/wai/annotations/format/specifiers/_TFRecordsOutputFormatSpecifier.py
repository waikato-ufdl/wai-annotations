from typing import Type

from ...core.component import LocalWriter, OutputConverter
from ...core.specifier import OutputFormatSpecifier, DomainSpecifier


class TFRecordsOutputFormatSpecifier(OutputFormatSpecifier):
    """
    Specifier of the components for writing the binary TFRecords
    object detection format.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes image object-detection annotations in the TFRecords binary format"

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier

    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        from ..tf.convert import ToTensorflowExample
        return ToTensorflowExample

    @classmethod
    def writer(cls) -> Type[LocalWriter]:
        from ..tf.io import TensorflowExampleWriter
        return TensorflowExampleWriter
