from wai.json.object import JSONObject
from wai.json.object.property import BoolProperty


class ImageQuality(JSONObject["ImageQuality"]):
    good_illumination: bool = BoolProperty(optional=True)
    blur: bool = BoolProperty(optional=True)
    frontal: bool = BoolProperty(optional=True)
