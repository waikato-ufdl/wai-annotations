from typing import List

from wai.common.json.configuration import Configuration, SubConfiguration
from wai.common.json.configuration.property import ArrayProperty

from ._Info import Info
from ._Image import Image
from ._Annotation import Annotation
from ._License import License
from ._Category import Category


class COCOFile(Configuration["COCOFile"]):
    info: Info = SubConfiguration("", Info)
    images: List[Image] = ArrayProperty(SubConfiguration("", Image))
    annotations: List[Annotation] = ArrayProperty(SubConfiguration("", Annotation))
    licenses: List[License] = ArrayProperty(SubConfiguration("", License))
    categories: List[Category] = ArrayProperty(SubConfiguration("", Category))
