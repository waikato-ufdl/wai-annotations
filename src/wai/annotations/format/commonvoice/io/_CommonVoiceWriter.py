import csv
from typing import Iterable

from ....core.component import SeparateFileWriter
from ....domain.audio import AudioInfo
from ..util import CommonVoiceDialect, EXPECTED_HEADER
from .._format import CommonVoiceFormat


class CommonVoiceWriter(SeparateFileWriter[CommonVoiceFormat]):
    """
    Writer of Mozilla's CommonVoice speech annotation format.
    """
    def write_annotations_only(self, instances: Iterable[CommonVoiceFormat], path: str):
        # Split the header into an iterable for DictWriter
        header = EXPECTED_HEADER.split('\t')

        with open(path, 'w') as file:
            # Create a TSV writer using the header
            csv_writer = csv.DictWriter(file, header, dialect=CommonVoiceDialect)

            # Write the header to file
            csv_writer.writeheader()

            # Write each annotated instance
            for instance in instances:
                # The attributes of CommonVoiceFormat are already the required types,
                # except for path, which is in the file-info object
                instance_dict = {name: getattr(instance, name)
                                 for name in header
                                 if name != "path"}
                instance_dict["path"] = instance.file.filename

                # Write the instance to the file
                csv_writer.writerow(instance_dict)

    @classmethod
    def output_help_text(cls) -> str:
        return "the filename of the TSV file to write the annotations into"

    def expects_file(self) -> bool:
        return True

    def extract_file_info_from_external_format(self, instance: CommonVoiceFormat) -> AudioInfo:
        return instance.file
