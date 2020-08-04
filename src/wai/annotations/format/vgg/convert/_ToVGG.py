from typing import Iterator

from ....core.component import OutputConverter
from ....domain.image.object_detection import ObjectDetectionInstance
from ....domain.image.object_detection.util import get_object_label, get_object_prefix
from ..configuration import *
from .._format import VGGExternalFormat
from ..utils import get_shape_attributes


class ToVGG(OutputConverter[ObjectDetectionInstance, VGGExternalFormat]):
    """
    Converter from internal format to VGG annotations.
    """
    def convert(self, instance: ObjectDetectionInstance) -> Iterator[VGGExternalFormat]:
        image_info, located_objects = instance

        # Create a region for each located object
        regions = [Region(region_attributes=RegionAttributes(name=f"{get_object_prefix(located_object)}-{index}",
                                                             type=get_object_label(located_object),
                                                             image_quality=ImageQuality()),
                          shape_attributes=get_shape_attributes(located_object))
                   for index, located_object in enumerate(located_objects, 1)]

        # Create an image info for the image
        image = Image(filename=image_info.filename,
                      size=-1,
                      file_attributes=FileAttributes(caption="", public_domain="no", image_url=""),
                      regions=regions)

        yield image_info, image
