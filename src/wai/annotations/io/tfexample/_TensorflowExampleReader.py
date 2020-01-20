from typing import Iterator

import tensorflow as tf

from ...core import Reader, ImageInfo
from ...core.external_formats import TensorflowExampleExternalFormat
from ...tf_utils import ShardCompactor, is_shard_filename, get_all_sharded_filenames, negative_example


class TensorflowExampleReader(Reader[TensorflowExampleExternalFormat]):
    """
    Reader of Tensorflow Example records.
    """
    def annotation_files(self) -> Iterator[str]:
        # Make sure each set of sharded files only appears once
        return ShardCompactor().process(super().annotation_files())

    def read_annotation_file(self, filename: str) -> Iterator[TensorflowExampleExternalFormat]:
        # Recurse if given a shard filename
        if is_shard_filename(filename):
            for shard_filename in get_all_sharded_filenames(filename):
                yield self.read_annotation_file(shard_filename)
            return

        # Load the record file
        dataset = tf.data.TFRecordDataset([filename])

        # Extract each example and yield
        for record in dataset:
            # Create the instance
            instance: TensorflowExampleExternalFormat = tf.train.Example()

            # Parse the record
            instance.ParseFromString(record.numpy())

            yield instance

    def image_info_to_external_format(self, image_info: ImageInfo) -> TensorflowExampleExternalFormat:
        return negative_example(image_info)
