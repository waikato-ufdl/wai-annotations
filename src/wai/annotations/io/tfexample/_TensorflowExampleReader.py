from typing import Iterable, Iterator

import tensorflow as tf

from ...core import Reader
from ...core.external_formats import TensorflowExampleExternalFormat
from ...tf_utils import sharded_filename_params, format_sharded_filename


class TensorflowExampleReader(Reader[TensorflowExampleExternalFormat]):
    """
    Reader of Tensorflow Example records.
    """
    def determine_input_files(self, input_path: str) -> Iterable[str]:
        # Treat the file as a shard file
        base_path, shards, index = sharded_filename_params(input_path)

        # If it's not a sharded filename, return the path itself
        if shards == 0:
            return input_path,

        # If it is a sharded filename, iterate over all matching shards
        return (format_sharded_filename(base_path, shards, index) for index in range(shards))

    @classmethod
    def input_help_text(cls) -> str:
        return "tensorflow records file (if sharded, any of the shard files)"

    def read(self, filename: str) -> Iterator[TensorflowExampleExternalFormat]:
        # Load the record file
        dataset = tf.data.TFRecordDataset([filename])

        # Extract each example and yield
        for record in dataset:
            # Create the instance
            instance: TensorflowExampleExternalFormat = tf.train.Example()

            # Parse the record
            instance.ParseFromString(record.numpy())

            yield instance
