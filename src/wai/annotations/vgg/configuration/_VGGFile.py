from wai.json.object import JSONObject
from wai.json.object.property import Property

from ._Image import Image


class VGGFile(JSONObject["VGGFile"]):
    @classmethod
    def _additional_properties_validation(cls) -> Property:
        return Image.as_property(optional=True)
