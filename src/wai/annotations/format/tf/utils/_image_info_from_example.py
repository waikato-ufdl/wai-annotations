from ....domain.image import ImageInfo, ImageFormat
from .._format import TensorflowExampleExternalFormat
from ._extract_feature import extract_feature


def image_info_from_example(instance: TensorflowExampleExternalFormat):
    """
    Extracts an image-info object from a Tensorflow example.

    :param instance:    The Tensorflow example.
    :return:            The image-info.
    """
    image_filename = extract_feature(instance.features, 'image/filename')[0].decode("utf-8")
    image_data = extract_feature(instance.features, 'image/encoded')[0]
    image_width = extract_feature(instance.features, 'image/width')[0]
    image_height = extract_feature(instance.features, 'image/height')[0]
    image_format = ImageFormat.for_extension(extract_feature(instance.features, 'image/format')[0].decode("utf-8"))

    if not isinstance(image_width, int) or not isinstance(image_height, int):
        raise TypeError(f"Image dimensions not in expected format (integer)")

    return ImageInfo(image_filename, image_data, image_format, (image_width, image_height))
