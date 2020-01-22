import datetime
from typing import Iterable, Dict

from ...core import SeparateImageWriter, ImageInfo
from ..configuration import COCOFile, Image, Category, Info, License
from .._format import COCOExternalFormat

# The default name/url to use for the license if none is provided
DEFAULT_LICENSE_NAME: str = "default"
DEFAULT_LICENSE_URL: str = ""


class COCOWriter(SeparateImageWriter[COCOExternalFormat]):
    """
    Writer of COCO-format JSON files.
    """
    def __init__(self,
                 output: str,
                 no_images: bool = False,
                 license_name: str = "",
                 license_url: str = ""):
        super().__init__(output, no_images)

        self.license_name: str = license_name
        self.license_url: str = license_url

    def write_without_images(self, instances: Iterable[COCOExternalFormat], path: str):
        # Get the current time
        now = datetime.datetime.now()

        # Create a lookup from category name to id
        category_lookup: Dict[str, int] = {}

        # Keep track of annotation ID numbers
        next_annotation_id: int = 1

        # Create a COCO file to write into
        coco_file: COCOFile = COCOFile(info=Info(year=now.year,
                                                 version="",
                                                 description="Converted using wai.annotations",
                                                 contributor="",
                                                 url="",
                                                 date_created=str(now)),
                                       images=[],
                                       annotations=[],
                                       licenses=[self.create_license()],
                                       categories=[])

        # Write each instance
        for instance_index, instance in enumerate(instances, 1):
            # Unpack the instance
            image_info, annotations, labels, prefixes = instance

            # Create the image description
            image = Image(id=instance_index,
                          width=image_info.width(),
                          height=image_info.height(),
                          file_name=image_info.filename,
                          license=1,
                          flickr_url="",
                          coco_url="",
                          date_captured="")

            # Add the image description to the file
            coco_file.images.append(image)

            # Process each annotation
            for annotation, label, prefix in zip(annotations, labels, prefixes):
                # Create a category for this label if there isn't one already
                if label not in category_lookup:
                    category = Category(id=len(category_lookup) + 1,
                                        name=label,
                                        supercategory=prefix)

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

    def create_license(self) -> License:
        """
        Creates the license for the images if one is specified,
        or a default one if not.

        :return:    The license.
        """
        return License(id=1,
                       name=self.license_name if self.license_name != "" else DEFAULT_LICENSE_NAME,
                       url=self.license_url if self.license_url != "" else DEFAULT_LICENSE_URL)

    def extract_image_info_from_external_format(self, instance: COCOExternalFormat) -> ImageInfo:
        # Unpack the instance
        image_info, annotations, labels, prefixes = instance

        return image_info
