import os
from typing import Tuple, Dict

import numpy as np

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import ProcessState
from ....domain.image import Image
from ....domain.image.segmentation import ImageSegmentationInstance, ImageSegmentationAnnotation
from ....domain.image.segmentation.util import UnlabelledInputMixin, RelativeDataPathMixin
from ..util import LabelSeparatorMixin


class FromLayerSegments(
    RelativeDataPathMixin,
    UnlabelledInputMixin,
    LabelSeparatorMixin,
    ProcessorComponent[Tuple[str, bool], ImageSegmentationInstance]
):
    """
    Reads image-segmentation instances from files on disk where each
    label has its own binary image mask.
    """
    # Groups from the basename of the data image filename to a map from
    # label to label-image filename
    groups: Dict[str, Dict[str, str]] = ProcessState(lambda self: {})

    def process_element(
            self,
            element: Tuple[str, bool],
            then: ThenFunction[ImageSegmentationInstance],
            done: DoneFunction
    ):
        # Split the element
        filename, is_negative = element

        # If this is a negative image, forward it as a negative instance
        if is_negative:
            return then(ImageSegmentationInstance.negative(filename))

        # If this is a segment image, save it for later in a group under
        # the basename of its data image
        basename, extension = os.path.splitext(filename)
        for label in self.labels:
            suffix = f"{self.label_separator}{label}"
            if basename.endswith(suffix):
                data_basename = basename[:-len(suffix)]
                if data_basename not in self.groups:
                    self.groups[data_basename] = {}
                self.groups[data_basename][label] = filename
                return

        raise Exception(f"filename '{filename}' doesn't end in a known label")

    def finish(
            self,
            then: ThenFunction[ImageSegmentationInstance],
            done: DoneFunction
    ):
        for data_image_basename, label_image_filename_lookup in self.groups.items():
            # Find the base image
            data_image_filename = self.get_associated_image(data_image_basename)

            # Error if the data image couldn't be found
            if data_image_filename is None:
                raise Exception(f"Couldn't find data image {data_image_basename}")

            # Load the data image
            data_image = Image.from_file(data_image_filename)

            # Create a segmentation annotation
            annotation = ImageSegmentationAnnotation(self.labels, data_image.size)

            # Process labels in reverse-order, so lower-indexed labels take priority
            # (i.e. overwrite) higher-indexed labels
            for label in reversed(self.labels):
                # If there's no image for this label, skip it
                if label not in label_image_filename_lookup:
                    continue

                # Get the filename for this label
                label_image_filename = label_image_filename_lookup[label]

                # Load the label image
                label_image = Image.from_file(label_image_filename).pil_image

                # The image must be binary
                if label_image.mode != "1":
                    raise Exception(f"Label image is not binary ({label_image.mode})")

                # Convert the image to 8-bit mode to separate pixels
                label_image = label_image.convert("L")

                # Extract an array of the required shape from the image
                mask = np.fromstring(label_image.tobytes(), dtype=np.uint8)
                mask.resize(annotation.indices.shape)

                # Create a boolean array which selects the annotated pixels
                selector_array = mask != 0

                # Merge the current index set with the indices from this label
                annotation.indices = np.where(selector_array, np.uint16(self.label_lookup[label]), annotation.indices)

            then(ImageSegmentationInstance(data_image, annotation))

        done()
