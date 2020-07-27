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

    def sort_categories(self):
        """
        Sorts the categories in this file into alphabetical order.
        """
        # Get the categories in their current order
        categories = list(self.categories)

        # Sort them
        categories.sort(key=lambda category: category.name)

        # Create a remapping lookup table for the categories
        remap = {category.id: index for index, category in enumerate(categories, 1)}

        # Remap the category IDs in the annotations
        for annotation in self.annotations:
            annotation.category_id = remap[annotation.category_id]

        # Remap the categories themselves
        for category in categories:
            category.id = remap[category.id]

        # Reinsert the categories into the file in their sorted order
        self.categories = categories
