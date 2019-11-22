import os
import datetime
from argparse import ArgumentParser, Namespace
from typing import Iterable, Any, Dict

from ...coco_utils.configuration import COCOFile, Image, Category, Info
from ...core import Writer
from ...core.external_formats import COCOExternalFormat
from ...core.utils import get_image_size


class COCOWriter(Writer[COCOExternalFormat]):
    def __init__(self, output: str, no_images: bool = False):
        super().__init__(output)

        self.no_images: bool = no_images

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument("--no-images", action="store_true", required=False, dest="no_images",
                            help="skip the writing of images, outputting only the annotations")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(no_images=namespace.no_images)
        return kwargs

    @classmethod
    def output_help_text(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"

    def write(self, instances: Iterable[COCOExternalFormat], path: str):
        # Get the current time
        now = datetime.datetime.now()

        # Create a lookup from category name to id
        category_lookup: Dict[str, int] = {}

        # Keep track of annotation ID numbers
        next_annotation_id: int = 1

        # Determine the directory for images
        path = os.path.dirname(self.output)

        # Create a COCO file to write into
        coco_file: COCOFile = COCOFile(info=Info(year=now.year,
                                                 version="",
                                                 description="Converted using wai.annotations",
                                                 contributor="",
                                                 url="",
                                                 date_created=str(now)),
                                       images=[],
                                       annotations=[],
                                       licenses=[],
                                       categories=[])

        # Write each instance
        for instance_index, instance in enumerate(instances, 1):
            # Unpack the instance
            image_filename, image_data, image_filetype, annotations, labels = instance

            # Write the image
            if not self.no_images:
                with open(os.path.join(path, image_filename), "wb") as file:
                    file.write(image_data)

            # Get the dimensions of the image
            width, height = get_image_size(image_data)

            # Create the image description
            image = Image(id=instance_index,
                          width=width,
                          height=height,
                          file_name=image_filename,
                          license=0,
                          flickr_url="",
                          coco_url="",
                          date_captured="")

            # Add the image description to the file
            coco_file.images.append(image)

            # Process each annotation
            for annotation, label in zip(annotations, labels):
                # Create a category for this label if there isn't one already
                if label not in category_lookup:
                    category = Category(id=len(category_lookup) + 1,
                                        name=label,
                                        supercategory="")

                    category_lookup[label] = category.id

                    coco_file.categories.append(category)

                # Update the annotations IDs
                annotation.id = next_annotation_id
                next_annotation_id += 1
                annotation.image_id = image.id
                annotation.category_id = category_lookup[label]

                # Add the annotation
                coco_file.annotations.append(annotation)

        # Save the file
        coco_file.save_to_json_file(self.output)
