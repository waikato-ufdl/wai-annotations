import os
from typing import Iterator, Iterable

from ...coco_utils.configuration import COCOFile
from ...core import Reader, ImageInfo
from ...core.external_formats import COCOExternalFormat


class COCOReader(Reader[COCOExternalFormat]):
    """
    Reader of COCO-format JSON files.
    """
    def determine_input_files(self, input_path: str) -> Iterable[str]:
        return input_path,

    @classmethod
    def input_help_text(cls) -> str:
        return "JSON-format COCO annotations file"

    def read(self, filename: str) -> Iterator[COCOExternalFormat]:
        # Read in the file
        coco_file: COCOFile = COCOFile.load_from_json_file(filename)

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
