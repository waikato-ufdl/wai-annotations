from wai.common.json.configuration import Configuration
from wai.common.json.configuration.property import NumberProperty, StringProperty


class License(Configuration["License"]):
    id: int = NumberProperty(integer_only=True)
    name: str = StringProperty()
    url: str = StringProperty()
