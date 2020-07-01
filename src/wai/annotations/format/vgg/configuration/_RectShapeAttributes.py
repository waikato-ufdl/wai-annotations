from wai.json.object import JSONObject
from wai.json.object.property import ConstantProperty, NumberProperty


class RectShapeAttributes(JSONObject["RectShapeAttributes"]):
    name: str = ConstantProperty(value="rect")
    x: int = NumberProperty(integer_only=True)
    y: int = NumberProperty(integer_only=True)
    width: int = NumberProperty(integer_only=True)
    height: int = NumberProperty(integer_only=True)
