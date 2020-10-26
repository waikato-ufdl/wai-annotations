from typing import FrozenSet

import numpy as np

from wai.common.cli.options import TypedOption

from ....core.component import ProcessorComponent
from ....core.domain import Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....core.util import InstanceState
from ....domain.classification import Classification
from ....domain.image.segmentation import ImageSegmentationAnnotation


class RemoveClasses(
    RequiresNoFinalisation,
    ProcessorComponent[Instance, Instance]
):
    """
    Inline stream-processor which removes classes from the stream. If used with
    a classification stream, the entire instance is removed for matching classes.
    If used with an image-segmentation stream, classes that match are removed
    from the instances, but the instances themselves are not removed.
    """
    # The classes to remove
    classes = TypedOption(
        "-c", "--classes",
        type=str,
        nargs="+",
        help="the classes to remove",
        metavar="CLASS",
        required=True
    )

    # The set of classes to remove
    _class_set: FrozenSet[str] = InstanceState(lambda self: frozenset(self.classes))

    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        # Get the annotations
        annotations = element.annotations

        # If the annotations are a classification, forward only those
        # not in the specified classes
        if isinstance(annotations, Classification):
            if annotations.label not in self._class_set:
                then(element)

        # If the annotations are segments, remove labels from the annotations,
        # but always forward the instance
        elif isinstance(annotations, ImageSegmentationAnnotation):
            # Create the set of indices that correspond to the classes to remove
            class_indices = [
                index
                for index, label in enumerate(annotations.labels, 1)
                if label in self._class_set
            ]

            indices = annotations.indices
            for index in reversed(class_indices):
                subtract_array = np.select(
                    [indices == index, indices > index],
                    [np.uint16(index), np.uint16(1)],
                    np.uint16(0)
                )

                indices = indices - subtract_array

            annotations.indices = indices
            annotations.labels = [
                label
                for label in annotations.labels
                if label not in self._class_set
            ]

            then(element)

        # Any other type is an error
        else:
            raise Exception(
                f"Annotations of type {element.annotations_type()} aren't handled "
                f" by remove-classes"
            )