from wai.common.json.configuration import Configuration
from wai.common.json.configuration.property import NumberProperty, StringProperty


class Image(Configuration["Image"]):
    id: int = NumberProperty(integer_only=True)
    width: int = NumberProperty(integer_only=True)
    height: int = NumberProperty(integer_only=True)
    file_name: str = StringProperty()
    license: int = NumberProperty(integer_only=True)
    flickr_url: str = StringProperty()
    coco_url: str = StringProperty()
    date_captured: str = StringProperty()
