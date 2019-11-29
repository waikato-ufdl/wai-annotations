from typing import List

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

        located_objects = self.process_located_objects(lefts, rights, tops, bottoms, labels, image_width, image_height)

        return ImageInfo(image_filename, image_data, image_format, (image_width, image_height)), located_objects

    def process_located_objects(self,
                                lefts: List[float],
                                rights: List[float],
                                tops: List[float],
                                bottoms: List[float],
                                labels: List[str],
                                image_width: int,
                                image_height: int) -> LocatedObjects:
        """
        Processes the data from the Tensorflow example into a list of located objects.

        :param lefts:           The left bounds of the objects.
        :param rights:          The right bounds of the objects.
        :param tops:            The top bounds of the objects.
        :param bottoms:         The bottom bounds of the objects.
        :param labels:          The labels of the objects.
        :param image_width:     The width of the image.
        :param image_height:    The height of the image.
        :return:                The located objects.
        """
        # Create the empty located objects
        located_objects: LocatedObjects = LocatedObjects()

        # Process each object in turn
        for left, right, top, bottom, label in zip(lefts, rights, tops, bottoms, labels):
            # Calculate the denormalised coordinates of the object
            x = round(left * image_width)
            y = round(top * image_height)
            width = round(right * image_width) - x + 1
            height = round(bottom * image_height) - y + 1

            # Create the located object
            located_object: LocatedObject = LocatedObject(x, y, width, height, **{LABEL_METADATA_KEY: label,
                                                                                  PREFIX_METADATA_KEY: DEFAULT_PREFIX})

            # Add the object to the list
            located_objects.append(located_object)

        return located_objects
