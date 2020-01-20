import numpy as np
from PIL import Image


def image_to_numpyarray(image):
    """
    Method to convert the image into a numpy array with three channels.
    faster solution via np.fromstring found here:
    https://stackoverflow.com/a/42036542/4698227

    :param image: the image object to convert
    :type image: Image
    :return: the numpy array
    :rtype: nd.array
    """

    im_arr = np.fromstring(image.tobytes(), dtype=np.uint8)
    im_arr = im_arr.reshape((image.size[1], image.size[0], 3))
    return im_arr


def remove_alpha_channel(image):
    """
    Converts the Image object (RGBA or ARGB) to RGB. Just passes it through if already RGB.

    :param image: the image object to convert if necessary
    :type image: Image
    :return: the converted object
    :rtype: Image
    """
    if image.mode is 'RGBA' or 'ARGB':
        return image.convert('RGB')
    else:
        return image
