import datetime
import os
from typing import List, Dict

from wai.common.cli.options import TypedOption, FlagOption

from ....core.component.util import SplitSink, JSONFileWriter, SplitState, ExpectsFile
from ....core.stream.util import ProcessState
from ..configuration import *
from ..util import COCOExternalFormat


class COCOWriter(
    ExpectsFile,
    JSONFileWriter[COCOExternalFormat],
    SplitSink[COCOExternalFormat]
):
    """
    Writes annotations in the MS-COCO JSON format to disk.
    """
    license_name: str = TypedOption(
        "--license-name",
        type=str,
        default="default",
        help="the license of the images"
    )

    license_url: str = TypedOption(
        "--license-url",
        type=str,
        default="",
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

    _coco_file: COCOFile = SplitState(lambda self: self.create_empty_coco_file())

    _next_annotation_id: int = SplitState(lambda self: 1)

    _next_image_id: int = SplitState(lambda self: 1)

    _category_lookup: Dict[str, Category] = ProcessState(
        lambda self: {
            label: Category(id=index, name=label, supercategory=self.default_supercategory)
            for index, label in enumerate(self.categories, 1)
        }
    )

    def consume_element_for_split(
            self,
            element: COCOExternalFormat
    ):
        # Unpack the instance
        image_info, annotations, labels, prefixes = element

        # Write the image file
        self.write_data_file(image_info, self.get_split_path(self.split_label, self.output_path))

        # If this is a negative example, don't add it to the JSON file
        if len(annotations) == 0:
            return

        # Create the image description
        image = Image(id=self._next_image_id,
                      width=image_info.width,
                      height=image_info.height,
                      file_name=image_info.filename,
                      license=1,
                      flickr_url="",
                      coco_url="",
                      date_captured="")

        # Increment the image ID for this split
        self._next_image_id += 1

        # Add the image description to the file
        self._coco_file.images.append(image)

        # Process each annotation
        for annotation, label, prefix in zip(annotations, labels, prefixes):
            # Create a category for this label if there isn't one already
            if label not in self._category_lookup:
                if self.error_on_new_category:
                    raise Exception(f"Unspecified category: {label}")

                self._category_lookup[label] = Category(
                    id=len(self._category_lookup) + 1,
                    name=label,
                    supercategory=prefix
                )

            # Update the annotations IDs
            annotation.id = self._next_annotation_id
            self._next_annotation_id += 1
            annotation.image_id = image.id
            annotation.category_id = self._category_lookup[label].id

            # Add the annotation
            self._coco_file.annotations.append(annotation)

    def finish_split(self):
        # Create the list of categories
        categories = [category for category in self._category_lookup.values()]
        categories.sort(key=lambda category: category.id)

        # Add the list of categories to the file
        self._coco_file.categories = categories

        # Sort the categories if requested
        if self.should_sort_categories:
            self._coco_file.sort_categories()

        # Specify a sub-directory for the split
        split_path = self.get_split_path(self.split_label, self.output, True)

        # Save the JSON file
        self._coco_file.save_json_to_file(split_path, self.indent)

        # If the categories need to be written, do so
        self.write_category_output_file(self._coco_file, split_path)

    def create_license(self) -> License:
        """
        Creates the license for the images if one is specified,
        or a default one if not.

        :return:    The license.
        """
        return License(
            id=1,
            name=self.license_name,
            url=self.license_url
        )

    def create_empty_coco_file(self) -> COCOFile:
        """
        Creates a new, empty COCO file.
        """
        # Get a current timestamp
        now = datetime.datetime.now()

        return COCOFile(
            info=Info(
                year=now.year,
                version="",
                description="Converted using wai.annotations",
                contributor="",
                url="",
                date_created=str(now)
            ),
            images=[],
            annotations=[],
            licenses=[self.create_license()],
            categories=[]
        )

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"

    def write_category_output_file(self, coco_file: COCOFile, path: str):
        """
        Writes a comma-separated list of the categories in the given
        COCO file to disk.

        :param coco_file:   The file containing the categories.
        :param path:        The directory to write the categories-file to.
        """
        # If this option isn't selected, skip it
        if self.category_output_file is None:
            return

        # Create the full file-path for the categories file
        category_path = os.path.join(os.path.dirname(path), self.category_output_file)

        # Write the file
        with open(category_path, 'w') as category_output_file:
            category_output_file.write(
                ",".join(
                    category.name
                    for category in coco_file.categories)
            )
