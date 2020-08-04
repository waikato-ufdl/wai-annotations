from typing import Iterator

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ....core.component import InputConverter
from ....domain.image.object_detection import ObjectDetectionInstance
from ....domain.image.object_detection.util import set_object_label
from ..configuration import Region, PolygonShapeAttributes
from .._format import VGGExternalFormat
from ..utils import from_polygon_shape_attributes, from_rect_shape_attributes


class FromVGG(InputConverter[VGGExternalFormat, ObjectDetectionInstance]):
    """
    Converter from VGG annotations to internal format.
    """
    def convert(self, instance: VGGExternalFormat) -> Iterator[ObjectDetectionInstance]:
        # Unpack the external format
        image_info, image = instance

        yield ObjectDetectionInstance(image_info, LocatedObjects(map(self.to_located_object, image.regions)))

    @staticmethod
    def to_located_object(region: Region) -> LocatedObject:
        """
        Converts a VGG Region configuration to a located object.

        :param region:      The region.
        :return:            The located object.
        """
        # Get the object label
        label: str = region.region_attributes.type

        # Get the shape attributes
        if isinstance(region.shape_attributes, PolygonShapeAttributes):
            x, y, width, height, polygon = from_polygon_shape_attributes(region.shape_attributes)
        else:
            x, y, width, height = from_rect_shape_attributes(region.shape_attributes)
            polygon = None

        # Create the located object
        located_object = LocatedObject(x, y, width, height)
        set_object_label(located_object, label)

        # Add the polygon if there is one
        if polygon is not None:
            located_object.set_polygon(polygon)

        return located_object
