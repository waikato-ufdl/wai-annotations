from typing import Iterator


from .._ensure_available import tensorflow as tf

from ....core.component import LocalReader
from ....domain.image import ImageInfo
from .._format import TensorflowExampleExternalFormat
from ..utils import negative_example


class TensorflowExampleReader(LocalReader[TensorflowExampleExternalFormat]):
    """
    Reader of Tensorflow Example records.
    """
    def read_annotation_file(self, filename: str) -> Iterator[TensorflowExampleExternalFormat]:
        # Load the record file
        dataset = tf.data.TFRecordDataset([filename])

        # Extract each example and yield
        for record in dataset:
            # Create the instance
            instance: TensorflowExampleExternalFormat = tf.train.Example()

            # Parse the record
            instance.ParseFromString(record.numpy())

            yield instance

    def read_negative_file(self, filename: str) -> Iterator[TensorflowExampleExternalFormat]:
        return negative_example(ImageInfo.from_file(filename))
