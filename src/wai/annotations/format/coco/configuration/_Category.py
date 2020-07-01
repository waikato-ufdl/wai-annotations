from wai.json.object import JSONObject
from wai.json.object.property import NumberProperty, StringProperty


class Category(JSONObject["Category"]):
    id: int = NumberProperty(integer_only=True)
    name: str = StringProperty()
    supercategory: str = StringProperty()
