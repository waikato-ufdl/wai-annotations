import numpy as np

from wai.common.geometry import Polygon

from .....core.util import polygon_to_poly_array
from .....image_utils import polygon_to_mask


def mask_from_polygon(
        polygon: Polygon,
        image_width: int,
        image_height: int
) -> np.ndarray:
    """
    Creates a mask from an object's polygon. Based on code
    from:

    https://github.com/tensorflow/models/blob/master/research/object_detection/dataset_tools/create_coco_tf_record.py

    :param polygon:         The object's bounding polygon.
    :param image_width:     The width of the image.
    :param image_height:    The height of the image.
    :return:                An array covering the image, 1 inside the polygon and 0 outside.
    """
    # Create a Numpy array for the polygon
    poly_array = polygon_to_poly_array(polygon)

    # Run-length encode the polygon into a bitmask
    return polygon_to_mask([poly_array], image_width, image_height)
