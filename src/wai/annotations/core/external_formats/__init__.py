"""
Package defining the supported formats for conversion.
"""
from ._adams import ADAMSExternalFormat
from ._coco import COCOExternalFormat
from ._roi import ROIExternalFormat, ROIObject
from ._tensorflow_examples import TensorflowExampleExternalFormat
from ._typing import ExternalFormat
from ._vgg import VGGExternalFormat
