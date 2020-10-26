from abc import ABC
from typing import TypeVar

from wai.common import TwoWayDict
from wai.common.cli.options import TypedOption

from .....core.component import ProcessorComponent
from .....core.util import InstanceState
from .._ImageSegmentationInstance import ImageSegmentationInstance

ExternalFormat = TypeVar("ExternalFormat")


class UnlabelledInputConverter(ProcessorComponent[ExternalFormat, ImageSegmentationInstance], ABC):
    """
    Base-class for image-segmentation input converters which don't
    provide labels for their indexed classes.
    """
    # Mapping from indices to labels
    labels = TypedOption(
        "--labels",
        type=str,
        nargs="+",
        metavar="LABEL",
        help="specifies the labels for each index"
    )

    label_lookup: TwoWayDict[int, str] = InstanceState(lambda self: _initialise_label_lookup(self))


def _initialise_label_lookup(self: UnlabelledInputConverter) -> TwoWayDict[int, str]:
    """
    Initialises the lookup between labels/indices on first access.

    :return:    The initialised lookup.
    """
    # Create the lookup
    lookup = TwoWayDict[int, str]()

    # Add the labels
    for index, label in enumerate(self.labels, 1):
        lookup[index] = label

    return lookup
