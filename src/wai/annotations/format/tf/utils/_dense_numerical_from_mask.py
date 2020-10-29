import numpy as np


def dense_numerical_from_mask(mask: np.ndarray) -> np.ndarray:
    """
    Encodes a binary image mask in Tensorflow's dense numerical format, in place.

    :param mask:    The image mask.
    :return:        The encoded array.
    """
    mask.resize((mask.size,))
    return mask
