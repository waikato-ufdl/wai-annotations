from typing import List

from wai.common.json.configuration import Configuration, SubConfiguration
from wai.common.json.configuration.property import ArrayProperty

from ._Info import Info
from ._Image import Image
from ._Annotation import Annotation
from ._License import License
from ._Category import Category


class COCOFile(Configuration["COCOFile"]):
    info: Info = SubConfiguration(configuration_type=Info)
    images: List[Image] = ArrayProperty(
        element_property=SubConfiguration(configuration_type=Image)
    )
    annotations: List[Annotation] = ArrayProperty(
        element_property=SubConfiguration(configuration_type=Annotation)
    )
    licenses: List[License] = ArrayProperty(
        element_property=SubConfiguration(configuration_type=License)
    )
    categories: List[Category] = ArrayProperty(
        element_property=SubConfiguration(configuration_type=Category)
    )
