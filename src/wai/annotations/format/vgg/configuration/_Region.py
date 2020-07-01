from typing import Union

from wai.json.object import JSONObject
from wai.json.object.property import OneOfProperty

from ._RegionAttributes import RegionAttributes
from ._RectShapeAttributes import RectShapeAttributes
from ._PolygonShapeAttributes import PolygonShapeAttributes


class Region(JSONObject["Region"]):
    region_attributes: RegionAttributes = RegionAttributes.as_property()
    shape_attributes: Union[RectShapeAttributes, PolygonShapeAttributes] = OneOfProperty(
        sub_properties=(
            RectShapeAttributes.as_property(),
            PolygonShapeAttributes.as_property()
        )
    )
