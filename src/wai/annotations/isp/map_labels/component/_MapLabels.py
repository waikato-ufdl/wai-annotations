from typing import Optional, Dict

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.cli.options import TypedOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....core.util import InstanceState
from ....domain.image.object_detection import ImageObjectDetectionInstance
from ....domain.image.object_detection.util import get_object_label, set_object_label


class MapLabels(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, ImageObjectDetectionInstance]
):
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

    @InstanceState
    def label_table(self) -> Dict[str, str]:
        label_table = {}
        for map_string in self.label_mapping:
            old, new = map_string.split("=")

            # Make sure we don't double-map a label
            if old in label_table:
                raise ValueError(f"Multiple mappings specified for label '{old}': "
                                 f"{label_table[old]}, {new}")

            label_table[old] = new

        return label_table

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        # Apply the label mapping
        self.apply_label_mapping(element.annotations)

        then(element)

    def apply_label_mapping(self, located_objects: LocatedObjects):
        """
        Maps the labels in the located objects from their current value to
        their new value.

        :param located_objects:     The parsed objects
        """
        # Do nothing if no mapping provided
        if len(self.label_table) == 0:
            return

        # Process each object
        for located_object in located_objects:
            # Get the object's current label
            label: Optional[str] = get_object_label(located_object, None)

            # If the object doesn't have a label, skip it
            if label is None:
                continue

            # If there is a mapping for this label, change it
            if label in self.label_table:
                set_object_label(located_object, self.label_table[label])
