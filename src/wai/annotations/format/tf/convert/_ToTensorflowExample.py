import hashlib
from argparse import Namespace
from typing import Tuple, List, Dict, Union, Iterator

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.cli import OptionsList

from .._ensure_available import tensorflow as tf

from ....core.component import OutputConverter
from ....domain.image.object_detection import ObjectDetectionInstance
from ....domain.image.object_detection.util import get_object_label
from ..utils import make_feature, mask_from_polygon, negative_example
from .._format import TensorflowExampleExternalFormat


class ToTensorflowExample(OutputConverter[ObjectDetectionInstance, TensorflowExampleExternalFormat]):
    """
    Converter from the internal format to Tensorflow Examples.
    """
    def __init__(self, namespace: Union[Namespace, OptionsList, None] = None):
        super().__init__(namespace)

        # Lookup to keep track of the labels we've seen and the classes
        # we've assigned to them
        self._label_class_lookup: Dict[str, int] = {}

    def convert(self, instance: ObjectDetectionInstance) -> Iterator[TensorflowExampleExternalFormat]:
        image_info, located_objects = instance

        # Make sure we have an image
        if image_info.data is None:
            raise ValueError(f"Tensorflow records require image data")

        # If no annotations, return an empty example
        if len(located_objects) == 0:
            yield negative_example(image_info)
            return

        # Format and extract the relevant annotation parameters
        lefts, rights, tops, bottoms, labels, classes, masks, is_crowds, areas = \
            self.process_located_objects(located_objects, image_info.width, image_info.height)

        # Create the example features
        feature_dict = {
            'image/height': make_feature(image_info.height),
            'image/width': make_feature(image_info.width),
            'image/filename': make_feature(image_info.filename),
            'image/source_id': make_feature(image_info.filename),
            'image/encoded': make_feature(image_info.data),
            'image/format': make_feature(image_info.format.get_default_extension()),
            'image/key/sha256': make_feature(hashlib.sha256(image_info.data).hexdigest()),
            'image/object/bbox/xmin': make_feature(lefts),
            'image/object/bbox/xmax': make_feature(rights),
            'image/object/bbox/ymin': make_feature(tops),
            'image/object/bbox/ymax': make_feature(bottoms),
            'image/object/class/text': make_feature(labels),
            'image/object/class/label': make_feature(classes),
            'image/object/is_crowd': make_feature([1 if is_crowd else 0 for is_crowd in is_crowds]),
            'image/object/area': make_feature(areas)
        }

        # Add the masks if present
        if len(masks) > 0:
            feature_dict['image/object/mask'] = make_feature(masks)

        # Create and return the example
        yield tf.train.Example(
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
        List[bytes],
        List[bool],
        List[float]
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
                                        - is_crowd flags (always false)
                                        - areas
        """
        # Format and extract the relevant annotation parameters
        lefts = []
        rights = []
        tops = []
        bottoms = []
        labels = []
        classes = []
        masks = []
        is_crowds = []
        areas = []
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
                is_crowds.append(False)
                if located_object.has_polygon():
                    polygon = located_object.get_polygon()
                    masks.append(mask_from_polygon(polygon,
                                                   image_width,
                                                   image_height))
                    areas.append(polygon.area())
                else:
                    areas.append(located_object.get_rectangle().area())

        return lefts, rights, tops, bottoms, labels, classes, masks, is_crowds, areas
