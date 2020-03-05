from typing import List

from wai.json.object import JSONObject
from wai.json.object.property import StringProperty, NumberProperty, ArrayProperty

from ._FileAttributes import FileAttributes
from ._Region import Region


class Image(JSONObject["Image"]):
    filename: str = StringProperty()
    size: int = NumberProperty(integer_only=True)
    file_attributes: FileAttributes = FileAttributes.as_property()
    regions: List[Region] = ArrayProperty(
        element_property=Region.as_property()
    )
