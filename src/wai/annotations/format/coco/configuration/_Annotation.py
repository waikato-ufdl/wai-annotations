from typing import List

from wai.common.adams.imaging.locateobjects import LocatedObject

from wai.json.object import JSONObject
from wai.json.object.property import NumberProperty, ArrayProperty


class Annotation(JSONObject["Annotation"]):
    id: int = NumberProperty(integer_only=True)
    image_id: int = NumberProperty(integer_only=True)
    category_id: int = NumberProperty(integer_only=True)
    segmentation: List[List[float]] = ArrayProperty(
        element_property=ArrayProperty(
            element_property=NumberProperty()
        ),
        max_elements=1
    )
    area: float = NumberProperty()
    bbox: List[float] = ArrayProperty(
        element_property=NumberProperty(),
        min_elements=4,
        max_elements=4
    )
    iscrowd: int = NumberProperty(minimum=0, maximum=1, integer_only=True)

    @classmethod
    def from_located_object(cls, located_object: LocatedObject) -> 'Annotation':
        """
        Converts the located object into a COCO annotation.

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

        return cls(
            id=0,
            image_id=0,
            category_id=0,  # Will be calculated at write-time
            segmentation=[polygon] if len(polygon) > 0 else [],
            area=area,
            bbox=[
                float(located_object.x),
                float(located_object.y),
                float(located_object.width),
                float(located_object.height)
            ],
            iscrowd=0
        )
