from argparse import Namespace
from typing import Tuple, List, Dict, Union

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.cli import OptionsList

from .._ensure_available import tensorflow as tf

from ...core import ImageInfo
from ...core.components import InternalFormatConverter
from ...core.utils import get_object_label
from ..utils import make_feature, mask_from_polygon, negative_example
from .._format import TensorflowExampleExternalFormat


class ToTensorflowExample(InternalFormatConverter[TensorflowExampleExternalFormat]):
    """
    Converter from the internal format to Tensorflow Examples.
    """
    def __init__(self, namespace: Union[Namespace, OptionsList, None] = None):
        super().__init__(namespace)

        # Lookup to keep track of the labels we've seen and the classes
        # we've assigned to them
        self._label_class_lookup: Dict[str, int] = {label: index for index, label in enumerate(self.labels, 1)}

    def convert_unpacked(self,
                         image_info: ImageInfo,
                         located_objects: LocatedObjects) -> TensorflowExampleExternalFormat:
        # Make sure we have an image
        if image_info.data is None:
            raise ValueError(f"Tensorflow records require image data")

        # If no annotations, return an empty example
        if len(located_objects) == 0:
            return negative_example(image_info)

        # Format and extract the relevant annotation parameters
        lefts, rights, tops, bottoms, labels, classes, masks = self.process_located_objects(located_objects,
                                                                                            image_info.width(),
                                                                                            image_info.height())

        # Create the example features
        feature_dict = {
            'image/height': make_feature(image_info.height()),
            'image/width': make_feature(image_info.width()),
            'image/filename': make_feature(image_info.filename),
            'image/source_id': make_feature(image_info.filename),
            'image/encoded': make_feature(image_info.data),
            'image/format': make_feature(image_info.format.get_default_extension()),
            'image/object/bbox/xmin': make_feature(lefts),
            'image/object/bbox/xmax': make_feature(rights),
            'image/object/bbox/ymin': make_feature(tops),
            'image/object/bbox/ymax': make_feature(bottoms),
            'image/object/class/text': make_feature(labels),
            'image/object/class/label': make_feature(classes)
        }

        # Add the masks if present
        if len(masks) > 0:
            feature_dict['image/object/mask'] = make_feature(masks)

        # Create and return the example
        return tf.train.Example(
            features=tf.train.Features(
                feature=feature_dict
            )
        )

    def process_located_objects(self, located_objects: LocatedObjects, image_width: int, image_height: int) -> Tuple[
        List[float],
        List[float],
        List[float],
        List[float],
        List[bytes],
        List[int],
        List[bytes]
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
                                        - masks
        """
        # Format and extract the relevant annotation parameters
        lefts = []
        rights = []
        tops = []
        bottoms = []
        labels = []
        classes = []
        masks = []
        for located_object in located_objects:
            # Get the object label
            label = get_object_label(located_object)

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
                if located_object.has_polygon():
                    masks.append(mask_from_polygon(located_object.get_polygon(),
                                                   image_width,
                                                   image_height))

        return lefts, rights, tops, bottoms, labels, classes, masks
