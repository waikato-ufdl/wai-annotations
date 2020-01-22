from wai.common.json.configuration import Configuration
from wai.common.json.configuration.property import StringProperty


class FileAttributes(Configuration["FileAttributes"]):
    caption: str = StringProperty()
    public_domain: str = StringProperty()
    image_url: str = StringProperty()
