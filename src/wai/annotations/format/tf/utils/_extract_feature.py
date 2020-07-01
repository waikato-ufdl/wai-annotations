from typing import List, Union

from .._ensure_available import tensorflow as tf


def extract_feature(features: tf.train.Features, name: str) -> Union[List[bytes], List[int], List[float]]:
    """
    Extracts the feature with the given name from the given features.

    :param features:    The tensorflow features to extract from.
    :param name:        The name of the feature to extract.
    :return:            The feature value list, or an empty list
                        if the feature isn't present in the features.
    """
    # Check the feature exists
    if name not in features.feature:
        return []

    # Select the feature
    feature = features.feature[name]

    if len(feature.bytes_list.value) > 0:
        return list(map(bytes, feature.bytes_list.value))
    elif len(feature.int64_list.value) > 0:
        return list(map(int, feature.int64_list.value))
    elif len(feature.float_list.value) > 0:
        return list(map(float, feature.float_list.value))
    else:
        return []
