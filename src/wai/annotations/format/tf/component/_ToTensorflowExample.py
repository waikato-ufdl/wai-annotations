import hashlib
from typing import Tuple, List, Dict

import numpy as np

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.cli.options import FlagOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import ProcessState, RequiresNoFinalisation
from ....domain.image.object_detection import ImageObjectDetectionInstance
from ....domain.image.object_detection.util import get_object_label
from ....domain.image.segmentation.util import mask_from_polygon
from ..utils import (
    tensorflow as tf,
    make_feature,
    negative_example,
    TensorflowExampleExternalFormat,
    png_from_mask,
    dense_numerical_from_mask
)


class ToTensorflowExample(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, TensorflowExampleExternalFormat]
):
    """
    Converter from the internal format to Tensorflow Examples.
    """
    dense_format: bool = FlagOption(
        "--dense",
        help="outputs masks in the dense numerical format instead of PNG-encoded"
    )

    _label_class_lookup: Dict[str, int] = ProcessState(lambda self: {})

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[TensorflowExampleExternalFormat],
            done: DoneFunction
    ):
        image_info, located_objects = element

        # Make sure we have an image
        if image_info.data is None:
            raise ValueError(f"Tensorflow records require image data")

        # If no annotations, return an empty example
        if located_objects is None or len(located_objects) == 0:
            return then(negative_example(image_info))

        # Format and extract the relevant annotation parameters
        lefts, rights, tops, bottoms, labels, classes, masks, is_crowds, areas = \
            self.process_located_objects(located_objects, image_info.width, image_info.height)

        # Create the example features
        feature_dict = {
            'image/height': make_feature(image_info.height),
            'image/width': make_feature(image_info.width),
            'image/filename': make_feature(image_info.filename.encode("utf-8")),
            'image/source_id': make_feature(image_info.filename.encode("utf-8")),
            'image/encoded': make_feature(image_info.data),
            'image/format': make_feature(image_info.format.get_default_extension().encode("utf-8")),
            'image/key/sha256': make_feature(hashlib.sha256(image_info.data).hexdigest().encode("utf-8")),
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
            # Encode the masks based on the --dense option
            feature_dict['image/object/mask'] = (
                tf.train.Feature(float_list=tf.train.FloatList(value=np.concatenate(list(map(dense_numerical_from_mask, masks)))))
                if self.dense_format else
                make_feature(list(map(png_from_mask, masks)))
            )

        # Create and return the example
        then(
            tf.train.Example(
                features=tf.train.Features(
                    feature=feature_dict
                )
            )
        )

    def process_located_objects(self, located_objects: LocatedObjects, image_width: int, image_height: int) -> Tuple[
        List[float],
        List[float],
        List[float],
        List[float],
        List[bytes],
        List[int],
        List[np.ndarray],
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
                    masks.append(
                        mask_from_polygon(
                            polygon,
                            image_width,
                            image_height
                        )
                    )
                    areas.append(polygon.area())
                else:
                    # TODO: If some located objects have polygons and some don't,
                    #       the 'masks' list will be a different size to the others.
                    #       Resolve.
                    areas.append(float(located_object.get_rectangle().area()))

        return lefts, rights, tops, bottoms, labels, classes, masks, is_crowds, areas
