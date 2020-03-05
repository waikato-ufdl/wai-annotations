from typing import List

from wai.json.object import JSONObject
from wai.json.object.property import ArrayProperty

from ._Info import Info
from ._Image import Image
from ._Annotation import Annotation
from ._License import License
from ._Category import Category


class COCOFile(JSONObject["COCOFile"]):
    info: Info = Info.as_property()
    images: List[Image] = ArrayProperty(
        element_property=Image.as_property()
    )
    annotations: List[Annotation] = ArrayProperty(
        element_property=Annotation.as_property()
    )
    licenses: List[License] = ArrayProperty(
        element_property=License.as_property()
    )
    categories: List[Category] = ArrayProperty(
        element_property=Category.as_property()
    )
