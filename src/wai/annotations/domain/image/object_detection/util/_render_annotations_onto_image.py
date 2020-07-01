from io import BytesIO

import PIL

from wai.common.adams.imaging.locateobjects import LocatedObjects

from .....core.utils import polygon_to_poly_array
from .....image_utils import polygon_to_mask
from ..util import polygon_from_rectangle


def render_annotations_onto_image(image: bytes, annotations: LocatedObjects) -> bytes:
    """
    Renders each of the located objects onto the given image.

    :param image:           The image.
    :param annotations:     The located objects in the image.
    :return:                The rendered image.
    """
    # Load the image
    image = PIL.Image.open(BytesIO(image))

    # Get a polygon for each annotation
    polygons = [annotation.get_polygon()
                if annotation.has_polygon()
                else polygon_from_rectangle(annotation.get_rectangle())
                for annotation in annotations]

    # Convert each to an array
    polys = list(map(polygon_to_poly_array, polygons))

    # Create a bit-mask of the polygons
    mask = polygon_to_mask(polys, image.width, image.height)

    # Load the mask as an alpha image
    image_mask = PIL.Image.fromarray(128 + mask * 127)

    # Set the alpha on the original image as the mask
    image.putalpha(image_mask)

    # Save the rendered image into a buffer
    image_buffer = BytesIO()
    image.save(image_buffer, "png")

    return image_buffer.getvalue()
