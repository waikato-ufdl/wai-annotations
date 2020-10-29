from typing import List, Union

from ._ensure_available import tensorflow as tf


def make_feature(value: Union[bytes, int, float, List[bytes], List[int], List[float]]) \
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

    # Must have at least one element in the list
    if len(value) == 0:
        raise Exception("make_feature cannot handle length-zero lists, feature must be created manually")

    # Determine the argument and class to Feature from the element type
    if isinstance(value[0], int):
        arg_name, cls = "int64_list", tf.train.Int64List
    elif isinstance(value[0], bytes):
        arg_name, cls = "bytes_list", tf.train.BytesList
    elif isinstance(value[0], float):
        arg_name, cls = "float_list", tf.train.FloatList
    else:
        raise Exception(f"make_feature only handles int/bytes/float types, got {type(value[0])}")

    return tf.train.Feature(**{arg_name: cls(value=value)})
