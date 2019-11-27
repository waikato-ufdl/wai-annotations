from wai.common.json.configuration import Configuration, SubConfiguration
from wai.common.json.configuration.property import StringProperty

from ._ImageQuality import ImageQuality


class RegionAttributes(Configuration["RegionAttributes"]):
    name: str = StringProperty()
    type: str = StringProperty()
    image_quality: ImageQuality = SubConfiguration(configuration_type=ImageQuality)
