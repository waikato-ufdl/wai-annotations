from typing import List, Union

from .._ensure_available import tensorflow as tf


def make_feature(value: Union[str, bytes, int, float, List[str], List[bytes], List[int], List[float]]) \
        -> tf.train.Feature:
    """
    Creates a feature of the correct format for the given value.

    :param value:   The value to create a feature for. Can be a
                    string, bytes, int or float, or a list of such.
    :return:        The feature.
    """
    # Convert scalars into lists
    if not isinstance(value, list):
        value = [value]

    # Convert strings to bytes
    for index in range(len(value)):
        element = value[index]
        if isinstance(element, str):
            value[index] = element.encode("utf-8")

    # Determine the argument and class to Feature from the element type
    arg_name, cls = ("int64_list", tf.train.Int64List) if isinstance(value[0], int) else \
                    ("bytes_list", tf.train.BytesList) if isinstance(value[0], bytes) else \
                    ("float_list", tf.train.FloatList)

    return tf.train.Feature(**{arg_name: cls(value=value)})
