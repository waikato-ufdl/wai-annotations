import datetime
from typing import Iterable, Dict, List, Tuple

from wai.common.cli.options import TypedOption, FlagOption

from ....core.component import JSONWriter
from ....domain.image import ImageInfo
from ..configuration import COCOFile, Image, Category, Info, License
from .._format import COCOExternalFormat

# The default name/url to use for the license if none is provided
DEFAULT_LICENSE_NAME: str = "default"
DEFAULT_LICENSE_URL: str = ""


class COCOWriter(JSONWriter[COCOExternalFormat]):
    """
    Writer of COCO-format JSON files.
    """
    license_name: str = TypedOption(
        "--license-name",
        type=str,
        help="the license of the images"
    )

    license_url: str = TypedOption(
        "--license-url",
        type=str,
        help="the license of the images"
    )

    categories: List[str] = TypedOption(
        "--categories",
        type=str,
        nargs="+",
        help="defines the order of the categories",
        metavar="CATEGORY"
    )

    error_on_new_category: bool = FlagOption(
        "--error-on-new-category",
        help="whether unspecified categories should raise an error"
    )

    default_supercategory = TypedOption(
        "--default-supercategory",
        type=str,
        help="the supercategory to use for pre-defined categories",
        metavar="SUPERCATEGORY",
        default="Object"
    )

    should_sort_categories = FlagOption(
        "--sort-categories",
        help="whether to put the categories in alphabetical order"
    )

    category_output_file: str = TypedOption(
        "--category-output-file",
        type=str,
        help="file to write the categories into, as a simple comma-separated list",
        metavar="FILENAME"
    )

    def initialise_category_lookup(self) -> Tuple[List[Category], Dict[str, int]]:
        """
        Initialises the category lookup.
        """
        # Create the result objects
        categories, lookup = [], {}

        # Add each specified category
        for index, label in enumerate(self.categories, 1):
            # Create the JSON object
            category = Category(id=index, name=label, supercategory=self.default_supercategory)

            # Add its index to the lookup
            lookup[label] = index

            # Add the JSON object to the output
            categories.append(category)

        return categories, lookup

    def create_json_object(self, instances: Iterable[COCOExternalFormat]) -> COCOFile:
        # Get the current time
        now = datetime.datetime.now()

        # Create a lookup from category name to id
        categories, category_lookup = self.initialise_category_lookup()

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
                                       categories=categories)

        # Write each instance
        for instance_index, instance in enumerate(instances, 1):
            # Unpack the instance
            image_info, annotations, labels, prefixes = instance

            # Create the image description
            image = Image(id=instance_index,
                          width=image_info.width,
                          height=image_info.height,
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
                    if self.error_on_new_category:
                        raise Exception(f"Unspecified category: {label}")

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

        # Sort the categories if requested
        if self.should_sort_categories:
            coco_file.sort_categories()

        # If the categories need to be written, do so
        if self.category_output_file is not None:
            with open(self.category_output_file, 'w') as category_output_file:
                category_output_file.write(",".join(category.name for category in coco_file.categories))

        return coco_file

    def create_license(self) -> License:
        """
        Creates the license for the images if one is specified,
        or a default one if not.

        :return:    The license.
        """
        return License(id=1,
                       name=self.license_name if self.license_name is not None else DEFAULT_LICENSE_NAME,
                       url=self.license_url if self.license_url is not None else DEFAULT_LICENSE_URL)

    def extract_file_info_from_external_format(self, instance: COCOExternalFormat) -> ImageInfo:
        # Unpack the instance
        image_info, annotations, labels, prefixes = instance

        return image_info

    @classmethod
    def output_help_text(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"
