import os
from argparse import ArgumentParser, Namespace
from typing import Iterable, Any, Dict

from wai.common.file.report import save

from ...core import Writer
from ...core.external_formats import ADAMSExternalFormat
from .constants import EXTENSION


class ADAMSReportWriter(Writer[ADAMSExternalFormat]):
    def __init__(self, output: str, no_images: bool = False):
        super().__init__(output)

        self.no_images: bool = no_images

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument("--no-images", action="store_true", required=False, dest="no_images",
                            help="skip the writing of images, outputting only the report files")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(no_images=namespace.no_images)
        return kwargs

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
            image_filename, image_data, report = instance

            # Write the image
            if not self.no_images and image_data is not None:
                with open(os.path.join(path, image_filename), "wb") as file:
                    file.write(image_data)

            # Format the report filename
            report_filename = os.path.splitext(image_filename)[0] + EXTENSION

            # Save the report
            save(report, os.path.join(path, report_filename))
