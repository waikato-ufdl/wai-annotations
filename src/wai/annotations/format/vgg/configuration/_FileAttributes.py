from wai.json.object import JSONObject
from wai.json.object.property import StringProperty


class FileAttributes(JSONObject["FileAttributes"]):
    caption: str = StringProperty()
    public_domain: str = StringProperty()
    image_url: str = StringProperty()
