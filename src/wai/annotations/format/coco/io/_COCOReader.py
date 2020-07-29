import os
from typing import Iterator

from ....core.component import LocalReader
from ....domain.image import ImageInfo
from ..configuration import COCOFile
from .._format import COCOExternalFormat


class COCOReader(LocalReader[COCOExternalFormat]):
    """
    Reader of COCO-format JSON files.
    """
    def read_annotation_file(self, filename: str) -> Iterator[COCOExternalFormat]:
        # Read in the file
        coco_file: COCOFile = COCOFile.load_json_from_file(filename)

        # Get the mapping from category ID to label
        label_lookup = {category.id: category.name for category in coco_file.categories}

        # Get a mapping from category ID to prefix
        prefix_lookup = {category.id: category.supercategory for category in coco_file.categories}

        # Create the path to the directory
        path = os.path.dirname(filename)

        # Each image yields an instance
        for image in coco_file.images:
            # Get the image associated to this entry
            image_file = os.path.join(path, image.file_name)

            # Load the image
            image_data = None
            if os.path.exists(image_file):
                with open(image_file, "rb") as file:
                    image_data = file.read()

            # Create the image info object
            image_info = ImageInfo(image.file_name, image_data, size=(image.width, image.height))

            # Collect the annotations for this image
            annotations = [annotation for annotation in coco_file.annotations if annotation.image_id == image.id]

            # Get the labels from the categories
            labels = [label_lookup[annotation.category_id] for annotation in annotations]

            # Get the prefixes from the categories
            prefixes = [prefix_lookup[annotation.category_id] for annotation in annotations]

            yield image_info, annotations, labels, prefixes

    def read_negative_file(self, filename: str) -> Iterator[COCOExternalFormat]:
        yield ImageInfo.from_file(filename), [], [], []
