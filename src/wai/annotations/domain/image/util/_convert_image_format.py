import io

from PIL import Image

from ....image_utils import remove_alpha_channel


def convert_image_format(image_data: bytes, to_format: str) -> bytes:
    """
    Converts image data from one format to another.

    :param image_data:  The binary image data to convert.
    :param to_format:   The format to convert the image data to.
    """
    # Uppercase the format
    to_format = to_format.upper()

    # Read the image data into an image
    image = Image.open(io.BytesIO(image_data))

    # Abort if image already in format
    if image.format == to_format:
        return image_data

    # Can't have alpha channel in JPEG images
    if to_format == "JPEG":
        image = remove_alpha_channel(image)

    # Write the image to an in-memory buffer
    output_io = io.BytesIO()
    image.save(output_io, format=to_format)

    # Return the buffer's contents
    return output_io.getvalue()
