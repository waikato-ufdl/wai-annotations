from typing import List

from wai.json.object import JSONObject
from wai.json.object.property import ConstantProperty, NumberProperty, ArrayProperty


class PolygonShapeAttributes(JSONObject["PolygonShapeAttributes"]):
    name: str = ConstantProperty(value="polygon")
    all_points_x: List[int] = ArrayProperty(
        element_property=NumberProperty(integer_only=True)
    )
    all_points_y: List[int] = ArrayProperty(
        element_property=NumberProperty(integer_only=True)
    )
