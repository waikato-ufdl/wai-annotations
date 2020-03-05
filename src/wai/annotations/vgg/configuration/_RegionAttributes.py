from wai.json.object import JSONObject
from wai.json.object.property import StringProperty

from ._ImageQuality import ImageQuality


class RegionAttributes(JSONObject["RegionAttributes"]):
    name: str = StringProperty()
    type: str = StringProperty()
    image_quality: ImageQuality = ImageQuality.as_property()
