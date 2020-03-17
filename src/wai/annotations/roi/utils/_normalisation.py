"""
Module for functions relating to normalisation of values.
"""


def normalisation_constant(unnormalised: float, normalised: float) -> int:
    """
    Returns the constant used to normalise a value.

    :param unnormalised:    The unnormalised value.
    :param normalised:      The normalised value.
    :return:                The normalisation constant.
    """
    return round(unnormalised / normalised)


def normalisation_constant_multi(*values: float):
    """
    Calculates the normalisation constant from multiple pairs
    of unnormalised/normalised values, using the first pair
    where the normalised value is not zero.

    :param values:  The value pairs.
    :return:        The normalisation constant.
    """
    # Make sure we have at least one pair
    if len(values) < 2:
        raise ValueError("Must provide at least two values to calculate normalisation constant")

    # Check each pair except the last
    for unnormalised, normalised in zip(values[0:-2:2], values[1:-1:2]):
        if normalised != 0.0:
            return normalisation_constant(unnormalised, normalised)

    # If all other pairs fail, use the last pair
    return normalisation_constant(values[-2], values[-1])
