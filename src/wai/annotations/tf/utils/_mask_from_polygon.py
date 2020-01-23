import io

import PIL
import numpy as np
from wai.common.geometry import Polygon


def mask_from_polygon(polygon: Polygon, image_width: int, image_height: int) -> bytes:
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
