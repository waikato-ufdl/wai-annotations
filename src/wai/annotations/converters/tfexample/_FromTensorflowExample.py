from typing import List
import io

import numpy as np
from skimage import measure
import PIL
from wai.common.geometry import Polygon, Point
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ...core import ExternalFormatConverter, InternalFormat, ImageInfo, ImageFormat
from ...core.external_formats import TensorflowExampleExternalFormat
from ...core.constants import LABEL_METADATA_KEY, PREFIX_METADATA_KEY, DEFAULT_PREFIX
from ...tf_utils import extract_feature


class FromTensorflowExample(ExternalFormatConverter[TensorflowExampleExternalFormat]):
    """
    Converter from Tensorflow Examples to the internal format.
    """
    def _convert(self, instance: TensorflowExampleExternalFormat) -> InternalFormat:
        # Define a UTF-8 decoder
        def decode_utf_8(bytes_: bytes) -> str:
            return bytes_.decode("utf-8")

        # Extract the image data from the example instance
        image_filename = decode_utf_8(extract_feature(instance.features, 'image/filename')[0])
        image_data = extract_feature(instance.features, 'image/encoded')[0]
        image_width = extract_feature(instance.features, 'image/width')[0]
        image_height = extract_feature(instance.features, 'image/height')[0]
        image_format = ImageFormat.for_extension(extract_feature(instance.features, 'image/format')[0])

        # Extract the located object data from the instance
        lefts = extract_feature(instance.features, 'image/object/bbox/xmin')
        rights = extract_feature(instance.features, 'image/object/bbox/xmax')
        tops = extract_feature(instance.features, 'image/object/bbox/ymin')
        bottoms = extract_feature(instance.features, 'image/object/bbox/ymax')
        labels = list(map(decode_utf_8, extract_feature(instance.features, 'image/object/class/text')))

        # Extract the optional mask information
        masks = extract_feature(instance.features, 'image/object/mask')
        if len(masks) == 0:
            masks = [b""] * len(lefts)

        located_objects = self.process_located_objects(lefts, rights, tops, bottoms, labels, masks, image_width, image_height)

        return ImageInfo(image_filename, image_data, image_format, (image_width, image_height)), located_objects

    def process_located_objects(self,
                                lefts: List[float],
                                rights: List[float],
                                tops: List[float],
                                bottoms: List[float],
                                labels: List[str],
                                masks: List[bytes],
                                image_width: int,
                                image_height: int) -> LocatedObjects:
        """
        Processes the data from the Tensorflow example into a list of located objects.

        :param lefts:           The left bounds of the objects.
        :param rights:          The right bounds of the objects.
        :param tops:            The top bounds of the objects.
        :param bottoms:         The bottom bounds of the objects.
        :param labels:          The labels of the objects.
        :param masks:           The masks of the objects.
        :param image_width:     The width of the image.
        :param image_height:    The height of the image.
        :return:                The located objects.
        """
        # Create the empty located objects
        located_objects: LocatedObjects = LocatedObjects()

        # Process each object in turn
        for left, right, top, bottom, label, mask in zip(lefts, rights, tops, bottoms, labels, masks):
            # Calculate the denormalised coordinates of the object
            x = round(left * image_width)
            y = round(top * image_height)
            width = round(right * image_width) - x + 1
            height = round(bottom * image_height) - y + 1

            # Create the located object
            located_object: LocatedObject = LocatedObject(x, y, width, height, **{LABEL_METADATA_KEY: label,
                                                                                  PREFIX_METADATA_KEY: DEFAULT_PREFIX})

            if len(mask) != 0:
                located_object.set_polygon(self.polygon_from_mask(mask))

            # Add the object to the list
            located_objects.append(located_object)

        return located_objects

    def polygon_from_mask(self, mask: bytes) -> Polygon:
        """
        Converts the PNG format mask into a polygon.

        :param mask:    The PNG mask.
        :return:        A polygon.
        """
        # Decode the PNG
        image = PIL.Image.open(io.BytesIO(mask))

        # Convert to a bitmask
        binary_mask = np.asarray(image)

        # Use find_contours to find the (only) polygon in the bitmask
        poly_array = measure.find_contours(binary_mask, 0.9, "high")[0]

        # Convert to a Polygon
        polygon = Polygon()
        for p in range(poly_array.shape[0]):
            polygon.points.append(Point(int(round(poly_array[p, 1])), int(round(poly_array[p, 0]))))

        # Remove redundant line segments
        polygon.simplify()

        return polygon
