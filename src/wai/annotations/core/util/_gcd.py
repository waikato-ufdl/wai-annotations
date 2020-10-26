from math import gcd as gcd2


def gcd(v1: int, *values: int) -> int:
    """
    Calculates the GCD of multiple values.

    :param v1:      The first value.
    :param values:  Any additional values.
    :return:        The GCD of all values.
    """
    # Reduce with any additional values
    for value in values:
        v1 = gcd2(v1, value)

    return v1
