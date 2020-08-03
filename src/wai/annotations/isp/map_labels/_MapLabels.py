from argparse import Namespace
from typing import Iterable, Union, Any, Optional

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.cli import OptionsList
from wai.common.cli.options import TypedOption

from ...core.component import InlineStreamProcessor
from ...domain.image.object_detection import ObjectDetectionInstance
from ...domain.image.object_detection.util import get_object_label, set_object_label


class MapLabels(InlineStreamProcessor[ObjectDetectionInstance]):
    """
    Processes a stream of object-detection instances, mapping labels
    from one set to another.
    """
    label_mapping = TypedOption(
        "-m", "--mapping",
        type=str,
        metavar="old=new", action='concat',
        help="mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)"
    )

    def __init__(self,
                 _namespace: Union[Namespace, OptionsList, None] = None,
                 **internal: Any):
        super().__init__(_namespace, **internal)

        # Create the label mapping
        self._label_mapping = {}
        for map_string in self.label_mapping:
            old, new = map_string.split("=")

            # Make sure we don't double-map a label
            if old in self._label_mapping:
                raise ValueError(f"Multiple mappings specified for label '{old}': "
                                 f"{self._label_mapping[old]}, {new}")

            self._label_mapping[old] = new

    def _process_element(self, element: ObjectDetectionInstance) -> Iterable[ObjectDetectionInstance]:
        # Apply the label mapping
        self.apply_label_mapping(element.annotations)

        yield element

    def apply_label_mapping(self, located_objects: LocatedObjects):
        """
        Maps the labels in the located objects from their current value to
        their new value.

        :param located_objects:     The parsed objects
        """
        # Do nothing if no mapping provided
        if len(self._label_mapping) == 0:
            return

        # Process each object
        for located_object in located_objects:
            # Get the object's current label
            label: Optional[str] = get_object_label(located_object, None)

            # If the object doesn't have a label, skip it
            if label is None:
                continue

            # If there is a mapping for this label, change it
            if label in self._label_mapping:
                set_object_label(located_object, self._label_mapping[label])
