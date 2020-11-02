from abc import ABC

from wai.common import TwoWayDict
from wai.common.cli import OptionValueHandler
from wai.common.cli.options import TypedOption

from .....core.util import InstanceState


class UnlabelledInputMixin(OptionValueHandler, ABC):
    """
    Mixin class which provides labels for image segmentation formats.
    """
    # Mapping from indices to labels
    labels = TypedOption(
        "--labels",
        type=str,
        nargs="+",
        metavar="LABEL",
        required=True,
        help="specifies the labels for each index"
    )

    label_lookup: TwoWayDict[int, str] = InstanceState(lambda self: _initialise_label_lookup(self))


def _initialise_label_lookup(self: UnlabelledInputMixin) -> TwoWayDict[int, str]:
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
