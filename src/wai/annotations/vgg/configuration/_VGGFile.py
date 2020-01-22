from wai.common.json.configuration import Configuration, SubConfiguration
from wai.common.json.configuration.property import Property

from ._Image import Image


class VGGFile(Configuration["VGGFile"]):
    @classmethod
    def additional_properties_validation(cls) -> Property:
        return SubConfiguration(configuration_type=Image)
