from wai.common.json.configuration import Configuration
from wai.common.json.configuration.property import NumberProperty, StringProperty


class Info(Configuration["Info"]):
    year: int = NumberProperty(integer_only=True)
    version: str = StringProperty()
    description: str = StringProperty()
    contributor: str = StringProperty()
    url: str = StringProperty()
    date_created: str = StringProperty()
