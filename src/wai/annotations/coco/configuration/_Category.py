from wai.common.json.configuration import Configuration
from wai.common.json.configuration.property import NumberProperty, StringProperty


class Category(Configuration["Category"]):
    id: int = NumberProperty(integer_only=True)
    name: str = StringProperty()
    supercategory: str = StringProperty()
