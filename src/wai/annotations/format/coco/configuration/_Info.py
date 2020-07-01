from wai.json.object import JSONObject
from wai.json.object.property import NumberProperty, StringProperty


class Info(JSONObject["Info"]):
    year: int = NumberProperty(integer_only=True)
    version: str = StringProperty()
    description: str = StringProperty()
    contributor: str = StringProperty()
    url: str = StringProperty()
    date_created: str = StringProperty()
