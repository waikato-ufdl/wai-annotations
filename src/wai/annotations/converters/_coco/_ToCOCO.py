from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ...coco_utils.configuration import Annotation
from ...core import InternalFormatConverter, ImageFormat
from ...core.external_formats import COCOExternalFormat
from ...core.utils import get_object_label


class ToCOCO(InternalFormatConverter[COCOExternalFormat]):
    """
    Converter from internal format to COCO annotations.
    """
    def convert_unpacked(self,
                         image_filename: str,
                         image_data: bytes,
                         image_format: ImageFormat,
                         located_objects: LocatedObjects) -> COCOExternalFormat:
        return (image_filename, image_data, image_format,
                list(map(self.convert_located_object, located_objects)),
                list(map(get_object_label, located_objects)))

    def convert_located_object(self, located_object: LocatedObject) -> Annotation:
        """
        Converts the located object into COCO annotations.

        :param located_object:      The located object to convert.
        :return:                    The COCO object.
        """
        # Get the object's polygon if it has one
        polygon = []
        if located_object.has_polygon():
            for point in located_object.get_polygon():
                polygon.append(float(point.x))
                polygon.append(float(point.y))

        return Annotation(id=0, image_id=0, category_id=0,  # Will be calculated at write-time
                          segmentation=[polygon],
                          area=0.0,  # TODO Calculate actual area
                          bbox=[float(located_object.x), float(located_object.y),
                                float(located_object.width), float(located_object.height)],
                          iscrowd=0)
