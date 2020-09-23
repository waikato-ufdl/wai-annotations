from abc import ABC
from typing import TypeVar

from wai.common import TwoWayDict
from wai.common.cli.options import TypedOption

from .....core.component import InputConverter
from .._ImageSegmentationInstance import ImageSegmentationInstance

ExternalFormat = TypeVar("ExternalFormat")


class UnlabelledInputConverter(InputConverter[ExternalFormat, ImageSegmentationInstance], ABC):
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

    @property
    def label_lookup(self) -> TwoWayDict[int, str]:
        if not hasattr(self, "_label_lookup_field"):
            setattr(self, "_label_lookup_field", self._initialise_label_lookup())
        return getattr(self, "_label_lookup_field")

    def _initialise_label_lookup(self) -> TwoWayDict[int, str]:
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
