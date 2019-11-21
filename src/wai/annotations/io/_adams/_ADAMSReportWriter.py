import os
from typing import Iterable

from wai.common.file.report import save

from ...core import Writer
from ...core.external_formats import ADAMSExternalFormat
from .constants import EXTENSION


class ADAMSReportWriter(Writer[ADAMSExternalFormat]):
    @classmethod
    def output_help_text(cls) -> str:
        return "output directory to write files to"

    def write(self, instances: Iterable[ADAMSExternalFormat], path: str):
        # Path must be a directory
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory, or does not exist")

        # Write each instance
        for instance in instances:
            # Unpack the instance
            image_filename, image_data, image_filetype, report = instance

            # Write the file
            with open(os.path.join(path, image_filename), "wb") as file:
                file.write(image_data)

            # Format the report filename
            report_filename = os.path.splitext(image_filename)[0] + EXTENSION

            # Save the report
            save(report, os.path.join(path, report_filename))
