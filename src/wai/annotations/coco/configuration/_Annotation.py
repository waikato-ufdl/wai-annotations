from typing import List

from wai.common.json.configuration import Configuration
from wai.common.json.configuration.property import NumberProperty, ArrayProperty


class Annotation(Configuration["Annotation"]):
    id: int = NumberProperty(integer_only=True)
    image_id: int = NumberProperty(integer_only=True)
    category_id: int = NumberProperty(integer_only=True)
    segmentation: List[List[float]] = ArrayProperty(
        element_property=ArrayProperty(
            element_property=NumberProperty()
        ),
        max_elements=1
    )
    area: float = NumberProperty()
    bbox: List[float] = ArrayProperty(
        element_property=NumberProperty(),
        min_elements=4,
        max_elements=4
    )
    iscrowd: int = NumberProperty(minimum=0, maximum=1, integer_only=True)
