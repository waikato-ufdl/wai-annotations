import os
from typing import Iterable

from wai.annotations.core.instance import FileInfo
from ....core.component import LocalWriter
from ....domain.image.classification import ImageClassificationInstance


class SubDirWriter(LocalWriter[ImageClassificationInstance]):
    """
    Writes images into a separate sub-directory for each label.
    """
    @classmethod
    def output_help_text(cls) -> str:
        return "the directory to store the class directories in"

    def write_to_path(self, instances: Iterable[ImageClassificationInstance], path: str):
        for instance in instances:
            # Format the class sub-directory
            class_path = os.path.join(path, instance.annotations)

            # Make sure the class sub-directory exists
            if not os.path.exists(class_path):
                os.mkdir(class_path)

            # Write the image to the class sub-directory
            instance.file_info.write_data_if_present(class_path)

    def expects_file(self) -> bool:
        return False

    def extract_file_info_from_external_format(self, instance: ImageClassificationInstance) -> FileInfo:
        return instance.file_info
