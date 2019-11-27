from wai.common.json.configuration import Configuration
from wai.common.json.configuration.property import BoolProperty


class ImageQuality(Configuration["ImageQuality"]):
    good_illumination: bool = BoolProperty(optional=True)
    blur: bool = BoolProperty(optional=True)
    frontal: bool = BoolProperty(optional=True)
