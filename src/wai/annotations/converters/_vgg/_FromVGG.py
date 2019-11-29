from typing import Tuple

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Polygon, Point

from ...vgg_utils.configuration import Region, RectShapeAttributes, PolygonShapeAttributes
from ...core import ExternalFormatConverter, InternalFormat
from ...core.constants import LABEL_METADATA_KEY, PREFIX_METADATA_KEY, DEFAULT_PREFIX
from ...core.external_formats import VGGExternalFormat


class FromVGG(ExternalFormatConverter[VGGExternalFormat]):
    """
    Converter from VGG annotations to internal format.
    """
    def _convert(self, instance: VGGExternalFormat) -> InternalFormat:
        # Unpack the external format
        image_info, image = instance

        return image_info, LocatedObjects(map(self.to_located_object, image.regions))

    def to_located_object(self, region: Region) -> LocatedObject:
        """
        Converts a VGG Region configuration to a located object.

        :param region:      The region.
        :return:            The located object.
        """
        # Get the object label
        label: str = region.region_attributes.type

        # Get the shape attributes
        if isinstance(region.shape_attributes, PolygonShapeAttributes):
            x, y, width, height, polygon = self.from_polygon_shape_attributes(region.shape_attributes)
        else:
            x, y, width, height = self.from_rect_shape_attributes(region.shape_attributes)
            polygon = None

        # Create the located object
        located_object = LocatedObject(x, y, width, height, **{LABEL_METADATA_KEY: label,
                                                               PREFIX_METADATA_KEY: DEFAULT_PREFIX})

        # Add the polygon if there is one
        if polygon is not None:
            located_object.set_polygon(polygon)

        return located_object

    def from_polygon_shape_attributes(self, shape_attributes: PolygonShapeAttributes) -> \
            Tuple[int, int, int, int, Polygon]:
        """
        Gets the bounds and the polygon for a located object from
        the polygon shape attributes of a region.

        :param shape_attributes:    The shape attributes.
        :return:                    The x, y, width, height and polygon of the located object.
        """
        # Get the polygon
        polygon = Polygon(*(Point(x, y) for x, y in zip(shape_attributes.all_points_x, shape_attributes.all_points_y)))

        # Get the top/left coordinates
        x = min(shape_attributes.all_points_x)
        y = min(shape_attributes.all_points_y)

        # Get the width and height
        width = max(shape_attributes.all_points_x) - x + 1
        height = max(shape_attributes.all_points_y) - y + 1

        return x, y, width, height, polygon

    def from_rect_shape_attributes(self, shape_attributes: RectShapeAttributes) -> \
            Tuple[int, int, int, int]:
        """
        Gets the bounds for a located object from the
        rectangular shape attributes of a region.

        :param shape_attributes:    The shape attributes.
        :return:                    The x, y, width and height of the located object.
        """
        return shape_attributes.x, shape_attributes.y, shape_attributes.width, shape_attributes.height
