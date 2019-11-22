from wai.common.adams.imaging.locateobjects import LocatedObject

from ..constants import LABEL_METADATA_KEY, DEFAULT_LABEL


def get_object_label(located_object: LocatedObject) -> str:
    """
    Gets the label of a located object.

    :param located_object:  The located object.
    :return:                The object's label.
    """
    return located_object.metadata[LABEL_METADATA_KEY] \
        if LABEL_METADATA_KEY in located_object.metadata \
        else DEFAULT_LABEL
