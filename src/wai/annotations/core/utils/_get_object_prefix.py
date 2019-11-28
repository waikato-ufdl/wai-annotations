from wai.common.adams.imaging.locateobjects import LocatedObject

from ..constants import PREFIX_METADATA_KEY, DEFAULT_PREFIX


def get_object_prefix(located_object: LocatedObject) -> str:
    """
    Gets the prefix of a located object.

    :param located_object:  The located object.
    :return:                The object's prefix.
    """
    return located_object.metadata[PREFIX_METADATA_KEY] \
        if PREFIX_METADATA_KEY in located_object.metadata \
        else DEFAULT_PREFIX
