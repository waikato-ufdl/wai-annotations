"""
Package providing the built-in read/writer types.
"""
from ._adams import ADAMSReportReader, ADAMSReportWriter
from ._coco import COCOReader, COCOWriter
from ._roi import ROIReader, ROIWriter
from ._tfexample import TensorflowExampleReader, TensorflowExampleWriter
from ._vgg import VGGReader, VGGWriter
