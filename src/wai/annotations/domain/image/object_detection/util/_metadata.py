"""
Module for working with meta-data on located objects.
"""
from typing import Dict, Optional, TypeVar, Union

from wai.common.adams.imaging.locateobjects import LocatedObject
from wai.common.adams.imaging.locateobjects import constants

# The meta-data key for the label of a located object
LABEL_METADATA_KEY: str = "type"

# The default label to use if no 'type' present
DEFAULT_LABEL: str = "object"

# The meta-data key for the prefix of a located object
PREFIX_METADATA_KEY: str = "prefix"

# The default prefix to use if no 'prefix' present
DEFAULT_PREFIX: str = "Object"

# The set of reserved meta-data keys for internal use
RESERVED_METADATA_KEYS = frozenset((
    constants.KEY_X,
    constants.KEY_Y,
    constants.KEY_WIDTH,
    constants.KEY_HEIGHT,
    constants.KEY_LOCATION,
    constants.KEY_POLY_X,
    constants.KEY_POLY_Y,
    constants.KEY_INDEX,
    LABEL_METADATA_KEY,
    PREFIX_METADATA_KEY
))

# The type of the default value
DefaultType = TypeVar("DefaultType")


def object_has_label(located_object: LocatedObject) -> bool:
    """
    Whether the located object has a label set.

    :param located_object:  The located object.
    :return:                True if it has a label.
    """
    return LABEL_METADATA_KEY in located_object.metadata


def get_object_label(located_object: LocatedObject,
                     default: DefaultType = DEFAULT_LABEL) -> Union[str, DefaultType]:
    """
    Gets the label of a located object.

    :param located_object:  The located object.
    :param default:         The value to return if no label is set.
    :return:                The object's label, or the default if none is set.
    """
    if not object_has_label(located_object):
        return default

    return located_object.metadata[LABEL_METADATA_KEY]


def set_object_label(located_object: LocatedObject, label: Optional[str]):
    """
    Sets the label of a located object.

    :param located_object:  The located object.
    :param label:           The object's label.
    """
    if label is None:
        if LABEL_METADATA_KEY in located_object.metadata:
            del located_object.metadata[LABEL_METADATA_KEY]
    else:
        located_object.metadata[LABEL_METADATA_KEY] = label


def object_has_prefix(located_object: LocatedObject) -> bool:
    """
    Whether the located object has a prefix set.

    :param located_object:  The located object.
    :return:                True if it has a prefix.
    """
    return PREFIX_METADATA_KEY in located_object.metadata


def get_object_prefix(located_object: LocatedObject,
                      default: DefaultType = DEFAULT_PREFIX) -> Union[str, DefaultType]:
    """
    Gets the prefix of a located object.

    :param located_object:  The located object.
    :param default:         The value to return if no prefix is set.
    :return:                The object's prefix.
    """
    if not object_has_prefix(located_object):
        return default

    return located_object.metadata[PREFIX_METADATA_KEY]


def set_object_prefix(located_object: LocatedObject, prefix: Optional[str]):
    """
    Sets the prefix of a located object.

    :param located_object:  The located object.
    :param prefix:          The object's prefix.
    """
    if prefix is None:
        if PREFIX_METADATA_KEY in located_object.metadata:
            del located_object.metadata[PREFIX_METADATA_KEY]
    else:
        located_object.metadata[PREFIX_METADATA_KEY] = prefix


def get_object_metadata(located_object: LocatedObject) -> Dict[str, str]:
    """
    Gets the meta-data from the given object.

    :param located_object:  The located object.
    :return:                The object's meta-data.
    """
    # Get a copy of the object's meta-data
    metadata = located_object.metadata.copy()

    # Remove the reserved keys
    for reserved_key in RESERVED_METADATA_KEYS:
        if reserved_key in metadata:
            del metadata[reserved_key]

    return metadata


def set_object_metadata(located_object: LocatedObject, **metadata: Optional[str]):
    """
    Sets the meta-data on a located object.

    :param located_object:  The located object.
    :param metadata:        The meta-data to set.
    """
    for key, value in metadata.items():
        # Make sure a reserved key isn't used
        if key in RESERVED_METADATA_KEYS:
            raise NameError(f"'{key}' is a reserved meta-data key")

        # A value of None removes the meta-data
        if value is None:
            if key in located_object.metadata:
                del located_object.metadata[key]
        else:
            located_object.metadata[key] = value
