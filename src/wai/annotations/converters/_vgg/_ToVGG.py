from typing import Union

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ...vgg_utils.configuration import Image, FileAttributes, Region, RegionAttributes, ImageQuality, \
    RectShapeAttributes, PolygonShapeAttributes
from ...core import InternalFormatConverter, ImageInfo
from ...core.external_formats import VGGExternalFormat
from ...core.utils import get_object_label, get_object_prefix


class ToVGG(InternalFormatConverter[VGGExternalFormat]):
    """
    Converter from internal format to VGG annotations.
    """
    def convert_unpacked(self,
                         image_info: ImageInfo,
                         located_objects: LocatedObjects) -> VGGExternalFormat:
        # Create a region for each located object
        regions = [Region(region_attributes=RegionAttributes(name=f"{get_object_prefix(located_object)}-{index}",
                                                             type=get_object_label(located_object),
                                                             image_quality=ImageQuality()),
                          shape_attributes=self.get_shape_attributes(located_object))
                   for index, located_object in enumerate(located_objects, 1)]

        # Create an image info for the image
        image = Image(filename=image_info.filename,
                      size=-1,
                      file_attributes=FileAttributes(caption="", public_domain="no", image_url=""),
                      regions=regions)

        return image_info, image

    def get_shape_attributes(self, located_object: LocatedObject) -> Union[RectShapeAttributes, PolygonShapeAttributes]:
        """
        Gets the shape attributes of the given located object.
        The type of the attributes is determined by whether
        the object is in bbox or mask format.

        :param located_object:  The located object.
        :return:                The shape attributes.
        """
        # Mask format
        if located_object.has_polygon():
            return PolygonShapeAttributes(name="polygon",
                                          all_points_x=located_object.get_polygon_x(),
                                          all_points_y=located_object.get_polygon_y())
        # Bbox format
        else:
            return RectShapeAttributes(name="rect",
                                       x=located_object.x,
                                       y=located_object.y,
                                       width=located_object.width,
                                       height=located_object.height)
