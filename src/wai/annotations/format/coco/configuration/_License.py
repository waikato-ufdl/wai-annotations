from wai.json.object import JSONObject
from wai.json.object.property import NumberProperty, StringProperty


class License(JSONObject["License"]):
    id: int = NumberProperty(integer_only=True)
    name: str = StringProperty()
    url: str = StringProperty()
