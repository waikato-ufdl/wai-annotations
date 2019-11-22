from typing import Union

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ...vgg_utils.configuration import Image, FileAttributes, Region, RegionAttributes, ImageQuality, \
    RectShapeAttributes, PolygonShapeAttributes
from ...core import InternalFormatConverter, ImageFormat
from ...core.external_formats import VGGExternalFormat
from ...core.utils import get_object_label


class ToVGG(InternalFormatConverter[VGGExternalFormat]):
    """
    Converter from internal format to VGG annotations.
    """
    def convert_unpacked(self,
                         image_filename: str,
                         image_data: bytes,
                         image_format: ImageFormat,
                         located_objects: LocatedObjects) -> VGGExternalFormat:
        regions = []
        for located_object in located_objects:
            region = Region(region_attributes=RegionAttributes(name="",
                                                               type=get_object_label(located_object),
                                                               image_quality=ImageQuality()),
                            shape_attributes=self.get_shape_attributes(located_object))

            regions.append(region)

        image = Image(filename=image_filename,
                      size=-1,
                      file_attributes=FileAttributes(caption="", public_domain="no", image_url=""),
                      regions=regions)

        return image_data, image_format, image

    def get_shape_attributes(self, located_object: LocatedObject) -> Union[RectShapeAttributes, PolygonShapeAttributes]:
        """
        TODO
        :param located_object:
        :return:
        """
        if located_object.has_polygon():
            return PolygonShapeAttributes(name="polygon",
                                          all_points_x=located_object.get_polygon_x(),
                                          all_points_y=located_object.get_polygon_y())
        else:
            return RectShapeAttributes(name="rect",
                                       x=located_object.x,
                                       y=located_object.y,
                                       width=located_object.width,
                                       height=located_object.height)
