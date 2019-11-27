from typing import Union

from wai.common.json.configuration import Configuration, SubConfiguration
from wai.common.json.configuration.property import OneOfProperty

from ._RegionAttributes import RegionAttributes
from ._RectShapeAttributes import RectShapeAttributes
from ._PolygonShapeAttributes import PolygonShapeAttributes


class Region(Configuration["Region"]):
    region_attributes: RegionAttributes = SubConfiguration(configuration_type=RegionAttributes)
    shape_attributes: Union[RectShapeAttributes, PolygonShapeAttributes] = OneOfProperty(
        sub_properties=(
            SubConfiguration(configuration_type=RectShapeAttributes),
            SubConfiguration(configuration_type=PolygonShapeAttributes)
        )
    )
