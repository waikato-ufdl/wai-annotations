from ..utils import tensorflow as tf

from ....core.component.util import AnnotationFileProcessor
from ....core.stream import ThenFunction
from ....domain.image import Image
from ..utils import negative_example, TensorflowExampleExternalFormat


class TensorflowExampleReader(AnnotationFileProcessor[TensorflowExampleExternalFormat]):
    """
    Reader of Tensorflow Example records.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[TensorflowExampleExternalFormat]):
        # Load the record file
        dataset = tf.data.TFRecordDataset([filename])

        # Extract each example and yield
        for record in dataset:
            # Create the instance
            instance: TensorflowExampleExternalFormat = tf.train.Example()

            # Parse the record
            instance.ParseFromString(record.numpy())

            then(instance)

    def read_negative_file(self, filename: str, then: ThenFunction[TensorflowExampleExternalFormat]):
        then(negative_example(Image.from_file(filename)))
