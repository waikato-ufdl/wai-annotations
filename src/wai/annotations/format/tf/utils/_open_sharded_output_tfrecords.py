from typing import List

from .._ensure_available import tensorflow as tf


def open_sharded_output_tfrecords(exit_stack, file_names: List[str]):
    """
    Opens all TFRecord shards for writing and adds them to an exit stack.

    Based on: https://github.com/tensorflow/models/blob/b9ef963d1e84da0bb9c0a6039457c39a699ea149/research/object_detection/dataset_tools/tf_record_creation_util.py

    :param exit_stack:  A context2.ExitStack used to automatically closed
                        the TFRecords opened in this function.
    :param file_names:  The file-names for the shards.
    :return:            The list of opened TFRecords. Position k in the list
                        corresponds to shard k.
    """
    return [exit_stack.enter_context(tf.io.TFRecordWriter(file_name))
            for file_name in file_names]
