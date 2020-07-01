import io

import PIL
from wai.common.geometry import Polygon

from ....core.utils import polygon_to_poly_array
from ....image_utils import polygon_to_mask


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
    # Create a Numpy array for the polygon
    poly_array = polygon_to_poly_array(polygon)

    # Run-length encode the polygon into a bitmask
    binary_mask = polygon_to_mask([poly_array], image_width, image_height)

    # Write the bitmask into PNG format
    output_io = io.BytesIO()
    PIL.Image.fromarray(binary_mask).save(output_io, format="PNG")

    return output_io.getvalue()
