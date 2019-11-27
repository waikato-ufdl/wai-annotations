from typing import List

from wai.common.json.configuration import Configuration
from wai.common.json.configuration.property import ConstantProperty, NumberProperty, ArrayProperty


class PolygonShapeAttributes(Configuration["PolygonShapeAttributes"]):
    name: str = ConstantProperty(value="polygon")
    all_points_x: List[int] = ArrayProperty(
        element_property=NumberProperty(integer_only=True)
    )
    all_points_y: List[int] = ArrayProperty(
        element_property=NumberProperty(integer_only=True)
    )
