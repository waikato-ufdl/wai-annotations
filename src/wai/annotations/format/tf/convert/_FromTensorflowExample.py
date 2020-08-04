from typing import List, Iterator

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.cli.options import TypedOption

from ....core.component import InputConverter
from ....domain.image import ImageInfo
from ....domain.image.object_detection import ObjectDetectionInstance
from ....domain.image.object_detection.util import set_object_label
from ..utils import extract_feature, image_info_from_example, polygon_from_mask
from .._format import TensorflowExampleExternalFormat


class FromTensorflowExample(InputConverter[TensorflowExampleExternalFormat, ObjectDetectionInstance]):
    """
    Converter from Tensorflow Examples to the internal format.
    """
    mask_threshold = TypedOption(
        "--mask-threshold",
        type=float,
        default=0.9,
        metavar="THRESHOLD",
        help="the threshold to use when calculating polygons from masks"
    )

    sample_stride = TypedOption(
        "--sample-stride",
        type=int,
        default=1,
        metavar="STRIDE",
        help="the stride to use when calculating polygons from masks"
    )

    def convert(self, instance: TensorflowExampleExternalFormat) -> Iterator[ObjectDetectionInstance]:
        # Define a UTF-8 decoder
        def decode_utf_8(bytes_: bytes) -> str:
            return bytes_.decode("utf-8")

        # Extract the image data from the example instance
        image_info: ImageInfo = image_info_from_example(instance)

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

        located_objects = self.process_located_objects(lefts, rights, tops, bottoms,
                                                       labels, masks,
                                                       image_info.width, image_info.height)

        yield ObjectDetectionInstance(image_info, located_objects)

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
            located_object: LocatedObject = LocatedObject(x, y, width, height)
            set_object_label(located_object, label)

            if len(mask) != 0:
                located_object.set_polygon(
                    polygon_from_mask(
                        mask,
                        (left * image_width, top * image_height, right * image_width, bottom * image_height),
                        self.mask_threshold,
                        self.sample_stride
                    )
                )

            # Add the object to the list
            located_objects.append(located_object)

        return located_objects
