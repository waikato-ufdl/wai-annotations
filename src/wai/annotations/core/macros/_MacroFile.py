from wai.json.object import JSONObject
from wai.json.object.property import StringProperty, ArrayProperty


class MacroFile(JSONObject['MacroFile']):
    """
    Defines the JSON schema for the macros stored on disk.
    """
    @classmethod
    def _additional_properties_validation(cls) -> ArrayProperty:
        return ArrayProperty(
            element_property=StringProperty(),
            optional=True
        )
