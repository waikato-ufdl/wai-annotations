from typing import Tuple, List, Dict, Optional, Pattern

from wai.common.adams.imaging.locateobjects import LocatedObjects
import tensorflow as tf

from ...core import InternalFormatConverter, ImageFormat
from ...core.constants import LABEL_METADATA_KEY
from ...core.external_formats import TensorflowExampleExternalFormat
from ...core.utils import get_image_size
from ...tf_utils import make_feature


class ToTensorflowExample(InternalFormatConverter[TensorflowExampleExternalFormat]):
    """
    Converter from the internal format to Tensorflow Examples.
    """
    def __init__(self, labels: Optional[List[str]] = None, regex: Optional[Pattern] = None):
        super().__init__(labels, regex)

        # Lookup to keep track of the labels we've seen and the classes
        # we've assigned to them
        self._label_class_lookup: Dict[str, int] = {label: index for index, label in enumerate(self.labels, 1)} \
            if self.labels is not None else {}

    def convert_unpacked(self,
                         image_filename: str,
                         image_data: Optional[bytes],
                         located_objects: LocatedObjects) -> TensorflowExampleExternalFormat:
        # Make sure we have an image
        if image_data is None:
            raise ValueError(f"Tensorflow records require image data")

        # Get the dimensions of the image
        width, height = get_image_size(image_data)

        # Get the image format
        image_format = ImageFormat.for_filename(image_filename)

        # Format and extract the relevant annotation parameters
        lefts, rights, tops, bottoms, labels, classes = self.process_located_objects(located_objects,
                                                                                     width,
                                                                                     height)

        # Create and return the example
        return tf.train.Example(
            features=tf.train.Features(
                feature={
                    'image/height': make_feature(height),
                    'image/width': make_feature(width),
                    'image/filename': make_feature(image_filename),
                    'image/source_id': make_feature(image_filename),
                    'image/encoded': make_feature(image_data),
                    'image/format': make_feature(image_format.get_default_extension()),
                    'image/object/bbox/xmin': make_feature(lefts),
                    'image/object/bbox/xmax': make_feature(rights),
                    'image/object/bbox/ymin': make_feature(tops),
                    'image/object/bbox/ymax': make_feature(bottoms),
                    'image/object/class/text': make_feature(labels),
                    'image/object/class/label': make_feature(classes)
                }
            )
        )

    def process_located_objects(self, located_objects: LocatedObjects, image_width: int, image_height: int) -> Tuple[
        List[float],
        List[float],
        List[float],
        List[float],
        List[bytes],
        List[int]
    ]:
        """
        Processes the located objects into the format expected by Features.

        :param located_objects:     The located objects.
        :param image_width:         The width of the image.
        :param image_height:        The height of the image.
        :return:                    A tuple of lists of:
                                        - left bounds
                                        - right bounds
                                        - top bounds
                                        - bottom bounds
                                        - UTF-8 encoded class labels
                                        - class categories
        """
        # Format and extract the relevant annotation parameters
        lefts = []
        rights = []
        tops = []
        bottoms = []
        labels = []
        classes = []
        for located_object in located_objects:
            # Make sure the object has a label
            if LABEL_METADATA_KEY not in located_object.metadata:
                continue

            # Get the object label
            label = located_object.metadata[LABEL_METADATA_KEY]

            # Skip unknown labels if given a specific set, or add it
            # if using auto-labeling
            if label not in self._label_class_lookup:
                self._label_class_lookup[label] = len(self._label_class_lookup) + 1

            # Get the class
            class_ = self._label_class_lookup[label]

            # Normalise the boundary coordinates
            left = located_object.x / image_width
            right = (located_object.x + located_object.width - 1) / image_width
            top = located_object.y / image_height
            bottom = (located_object.y + located_object.height - 1) / image_height

            # Append the object to the lists if its kosher
            if (0.0 <= left < right <= 1.0) and (0.0 <= top < bottom <= 1.0):
                lefts.append(left)
                rights.append(right)
                tops.append(top)
                bottoms.append(bottom)
                labels.append(label.encode('utf-8'))
                classes.append(class_)

        return lefts, rights, tops, bottoms, labels, classes
