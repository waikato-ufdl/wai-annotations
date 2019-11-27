from typing import List

from wai.common.json.configuration import Configuration, SubConfiguration
from wai.common.json.configuration.property import StringProperty, NumberProperty, ArrayProperty

from ._FileAttributes import FileAttributes
from ._Region import Region


class Image(Configuration["Image"]):
    filename: str = StringProperty()
    size: int = NumberProperty(integer_only=True)
    file_attributes: FileAttributes = SubConfiguration(configuration_type=FileAttributes)
    regions: List[Region] = ArrayProperty(
        element_property=SubConfiguration(configuration_type=Region)
    )
