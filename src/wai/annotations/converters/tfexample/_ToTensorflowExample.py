import io
from typing import Tuple, List, Dict, Optional, Pattern

import PIL
import numpy as np
from wai.common.geometry import Polygon
from wai.common.adams.imaging.locateobjects import LocatedObjects
import tensorflow as tf

from ...core import InternalFormatConverter, ImageFormat, ImageInfo
from ...core.constants import LABEL_METADATA_KEY
from ...core.external_formats import TensorflowExampleExternalFormat
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
                         image_info: ImageInfo,
                         located_objects: LocatedObjects) -> TensorflowExampleExternalFormat:
        # Make sure we have an image
        if image_info.data is None:
            raise ValueError(f"Tensorflow records require image data")

        # Get the image format
        image_format = ImageFormat.for_filename(image_info.filename)

        # If no annotations, return an empty example
        if len(located_objects) == 0:
            return self.create_empty_example(image_info, image_format)

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
            'image/format': make_feature(image_format.get_default_extension()),
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
                if located_object.has_polygon():
                    masks.append(self.mask_from_polygon(located_object.get_polygon(),
                                                        image_width,
                                                        image_height))

        return lefts, rights, tops, bottoms, labels, classes, masks

    def create_empty_example(self, image_info: ImageInfo, image_format: ImageFormat):
        """
        Creates an empty example (for images with no annotations).

        :return:    The empty example.
        """
        return tf.train.Example(
            features=tf.train.Features(
                feature={
                    'image/height': make_feature(image_info.height()),
                    'image/width': make_feature(image_info.width()),
                    'image/filename': make_feature(image_info.filename),
                    'image/source_id': make_feature(image_info.filename),
                    'image/encoded': make_feature(image_info.data),
                    'image/format': make_feature(image_format.get_default_extension()),
                    'image/object/bbox/xmin': tf.train.Feature(float_list=tf.train.FloatList(value=[])),
                    'image/object/bbox/xmax': tf.train.Feature(float_list=tf.train.FloatList(value=[])),
                    'image/object/bbox/ymin': tf.train.Feature(float_list=tf.train.FloatList(value=[])),
                    'image/object/bbox/ymax': tf.train.Feature(float_list=tf.train.FloatList(value=[])),
                    'image/object/class/text': tf.train.Feature(bytes_list=tf.train.BytesList(value=[])),
                    'image/object/class/label': tf.train.Feature(int64_list=tf.train.Int64List(value=[])),
                    'image/object/mask': tf.train.Feature(bytes_list=tf.train.BytesList(value=[]))
                }
            )
        )

    def mask_from_polygon(self, polygon: Polygon, image_width: int, image_height: int) -> bytes:
        """
        Creates a mask from an object's polygon. Based on code
        from:

        https://github.com/tensorflow/models/blob/master/research/object_detection/dataset_tools/create_coco_tf_record.py

        :param polygon:         The object's bounding polygon.
        :param image_width:     The width of the image.
        :param image_height:    The height of the image.
        :return:                The mask data.
        """

        # Flatten the polygon points into a list
        poly_list = []
        for point in polygon:
            poly_list.append(point.x)
            poly_list.append(point.y)

        # Create a Numpy array for the polygon
        poly_array = np.array(poly_list, dtype=float)

        # Run-length encode the polygon into a bitmask
        from pycocotools import mask
        rle = mask.frPyObjects([poly_array], image_height, image_width)
        binary_mask = np.amax(mask.decode(rle), axis=2)

        # Write the bitmask into PNG format
        output_io = io.BytesIO()
        PIL.Image.fromarray(binary_mask).save(output_io, format="PNG")

        return output_io.getvalue()

