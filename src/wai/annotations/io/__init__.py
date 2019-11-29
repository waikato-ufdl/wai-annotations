"""
Package providing the built-in read/writer types.
"""
from .adams import ADAMSReportReader, ADAMSReportWriter
from .coco import COCOReader, COCOWriter
from .roi import ROIReader, ROIWriter
from .tfexample import TensorflowExampleReader, TensorflowExampleWriter
from .vgg import VGGReader, VGGWriter
