from wai.common.json.configuration import Configuration
from wai.common.json.configuration.property import ConstantProperty, NumberProperty


class RectShapeAttributes(Configuration["RectShapeAttributes"]):
    name: str = ConstantProperty(value="rect")
    x: int = NumberProperty(integer_only=True)
    y: int = NumberProperty(integer_only=True)
    width: int = NumberProperty(integer_only=True)
    height: int = NumberProperty(integer_only=True)
