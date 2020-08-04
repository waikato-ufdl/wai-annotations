from typing import Iterator

from wai.common.adams.imaging.locateobjects import LocatedObject

from ....core.component import OutputConverter
from ....domain.image.object_detection import ObjectDetectionInstance
from ....domain.image.object_detection.util import get_object_label, get_object_prefix
from ..configuration import Annotation
from .._format import COCOExternalFormat


class ToCOCO(OutputConverter[ObjectDetectionInstance, COCOExternalFormat]):
    """
    Converter from internal format to COCO annotations.
    """
    def convert(self, instance: ObjectDetectionInstance) -> Iterator[COCOExternalFormat]:
        image_info, located_objects = instance

        yield (image_info,
               list(map(self.convert_located_object, located_objects)),
               list(map(get_object_label, located_objects)),
               list(map(get_object_prefix, located_objects)))

    @staticmethod
    def convert_located_object(located_object: LocatedObject) -> Annotation:
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

        # Calculate the area of the annotation
        if located_object.has_polygon():
            area = located_object.get_polygon().area()
        else:
            area = float(located_object.get_rectangle().area())

        return Annotation(id=0, image_id=0, category_id=0,  # Will be calculated at write-time
                          segmentation=[polygon] if len(polygon) > 0 else [],
                          area=area,
                          bbox=[float(located_object.x), float(located_object.y),
                                float(located_object.width), float(located_object.height)],
                          iscrowd=0)
