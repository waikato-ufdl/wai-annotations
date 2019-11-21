"""
Module defining the components available to the main function.
"""
from typing import Dict, Optional, Tuple, Type

from ..core import Reader, ExternalFormatConverter, InternalFormatConverter, Writer
from ..converters import *
from ..io import *

# The type of a specification of the components for a single external format
ComponentSpec = Tuple[
    Optional[Type[Reader]],
    Optional[Type[ExternalFormatConverter]],
    Optional[Type[InternalFormatConverter]],
    Optional[Type[Writer]]
]

components: Dict[str, ComponentSpec] = {
    "adams": (ADAMSReportReader, FromADAMSReport, ToADAMSReport, ADAMSReportWriter),
    "tfrecords": (None, FromTensorflowExample, ToTensorflowExample, TensorflowExampleWriter)
}
