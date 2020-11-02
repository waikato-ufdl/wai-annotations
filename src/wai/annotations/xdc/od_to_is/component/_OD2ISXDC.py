import numpy as np

from wai.common.cli.options import FlagOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import ProcessState, RequiresNoFinalisation
from ....domain.image.object_detection import ImageObjectDetectionInstance
from ....domain.image.object_detection.util import get_object_label
from ....domain.image.segmentation import ImageSegmentationInstance, ImageSegmentationAnnotation
from ....domain.image.segmentation.util import UnlabelledInputMixin, mask_from_rectangle, mask_from_polygon


class OD2ISXDC(
    RequiresNoFinalisation,
    UnlabelledInputMixin,
    ProcessorComponent[ImageObjectDetectionInstance, ImageSegmentationInstance]
):
    """
    Cross-domain converter from the image object-detection domain to the
    image segmentation domain.
    """
    error_on_unspecified_label: bool = FlagOption(
        "--label-error",
        help="whether to raise errors when an unspecified label is encountered "
             "(default is to ignore)"
    )

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ImageSegmentationInstance],
            done: DoneFunction
    ):
        # If the instance is a negative, leave it as one
        if element.annotations is None:
            return then(ImageSegmentationInstance(element.data, None))

        # Create an empty segmentation annotation
        annotation = ImageSegmentationAnnotation(self.labels, element.data.size)

        # Segment labels in reverse definition order so that lower-priority annotations
        # are overridden by higher-priority ones
        for label in reversed(self.labels):
            for located_object in element.annotations:
                # Get the label for the located object
                located_object_label = get_object_label(located_object)

                # Check for unspecified labels
                if self.error_on_unspecified_label and located_object_label not in self.label_lookup:
                    raise Exception(f"Unspecified label '{located_object_label}'")

                # If it's not the current label, leave it for later
                if located_object_label != label:
                    continue

                # Get the mask for the object's bounds
                mask = mask_from_polygon(located_object.get_polygon(), annotation.size[0], annotation.size[1]) \
                    if located_object.has_polygon() else \
                    mask_from_rectangle(located_object.get_rectangle(), annotation.size[0], annotation.size[1])

                # Mix the mask in with the segmentation so far
                annotation.indices = np.where(mask, np.uint16(self.label_lookup[label]), annotation.indices)

        then(ImageSegmentationInstance(element.data, annotation))
